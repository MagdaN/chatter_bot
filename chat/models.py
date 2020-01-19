import yaml
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey


def training_path(instance, filename):
    return 'training/{0}.txt'.format(instance.name)


class Conversation(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True)
    file = models.FileField(upload_to=training_path)

    class Meta:
        ordering = ('created', )
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversation')

    def __str__(self):
        return self.name

    def train(self):
        Statement.objects.filter(conversation=self).delete()

        with self.file.open() as f:
            statements = yaml.safe_load(f.read())
            self.train_statement(statements)

    def train_statement(self, training_statements, parent=None):
        for training_statement in training_statements:
            statement = Statement(
                parent=parent,
                conversation=self,
                request=training_statement['request'],
                response=training_statement['response'])
            statement.save()

            if 'children' in training_statement:
                self.train_statement(training_statement['children'], parent=statement)


@receiver(post_save, sender=Conversation)
def handle_conversation_save(sender, instance, created, **kwargs):
    instance.train()


@receiver(post_delete, sender=Conversation)
def handle_conversation_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class Statement(MPTTModel):

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='statements')

    request = models.TextField()
    response = models.TextField()

    def __str__(self):
        return self.request

    class Meta:
        ordering = ('conversation', )
        verbose_name = _('Statement')
        verbose_name_plural = _('Statements')

    @property
    def is_root(self):
        return self.parent is None
