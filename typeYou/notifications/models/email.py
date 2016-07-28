from django.db import models

from .base import BaseNotification


class EmailNotification(BaseNotification):

    class Meta:
        verbose_name = 'Email Notification'
        verbose_name_plural = 'Email Notification'

    def send_notification(self):
        from notifications.tasks import SendEmailTask
        email = SendEmailTask()
        email.delay(self.id)
