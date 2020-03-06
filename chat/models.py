import os

import yaml
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey


def training_path(instance, file_name):
    return os.path.join('training', file_name)


class Conversation(TimeStampedModel):

    name = models.CharField(max_length=64, blank=True)
    file = models.FileField(upload_to=training_path)

    class Meta:
        ordering = ('created', )
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversation')

    def __str__(self):
        return self.name

    def save(self):
        basename = os.path.basename(self.file.name)
        root, ext = os.path.splitext(basename)
        self.name = root.split('_')[0]
        super().save()

    def clean(self):
        try:
            yaml.safe_load(self.file.open().read())
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
            raise ValidationError(e)

    def train(self):
        Statement.objects.filter(conversation=self).delete()

        with self.file.open() as f:
            statement = yaml.safe_load(f.read())
            self.train_statement(statement)

    def train_statement(self, training_statement, parent=None):
        if 'message' in training_statement:
            statement = Statement(
                parent=parent,
                conversation=self,
                message=training_statement['message'],
                reply=training_statement.get('reply', ''),
                conclusion=training_statement.get('conclusion', ''),
                forward=training_statement.get('forward', ''),
                reference=training_statement.get('reference', '')
            )
            statement.save()

            if 'children' in training_statement:
                for child_statement in training_statement['children']:
                    self.train_statement(child_statement, parent=statement)


@receiver(post_save, sender=Conversation)
def handle_conversation_save(sender, instance, created, **kwargs):
    if not kwargs.get('raw'):
        instance.train()


@receiver(post_delete, sender=Conversation)
def handle_conversation_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class Statement(MPTTModel):

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='statements')

    message = models.TextField()
    reply = models.TextField(default='', blank=True)
    conclusion = models.TextField(default='', blank=True)
    forward = models.TextField(default='', blank=True)
    reference = models.TextField(default='', blank=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('conversation', )
        verbose_name = _('Statement')
        verbose_name_plural = _('Statements')

    @property
    def is_root(self):
        return self.parent is None

    @property
    def get_conclusion(self):
        if not self.children.exists() and not self.conclusion and not self.forward:
            self.conclusion = settings.REPLIES.get('conclusion')
