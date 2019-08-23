from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django_extensions.db.models import TimeStampedModel

from .training import train_file

def training_path(instance, filename):
    return 'training/{0}.txt'.format(instance.name)


class TrainingFile(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True)
    file = models.FileField(upload_to=training_path)

    class Meta:
        ordering = ('created', )
        verbose_name = _('TrainingFile')
        verbose_name_plural = _('TrainingFiles')

    def __str__(self):
        return self.name

    def train(self):
        train_file(self.name, self.file.open('r'))


@receiver(post_save, sender=TrainingFile)
def handle_training_file_save(sender, instance, created, **kwargs):
    if created:
        instance.train()


@receiver(post_delete, sender=TrainingFile)
def handle_training_file_delete(sender, instance, **kwargs):
    instance.file.delete(False)
