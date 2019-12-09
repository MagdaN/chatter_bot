from django.contrib import admin
from django.utils.translation import gettext as _

from .models import TrainingFile


def train(modeladmin, request, queryset):
    for instance in queryset:
        instance.train()


train.short_description = _('Train selected TrainingFiles again')


@admin.register(TrainingFile)
class TrainingFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    actions = [train]
