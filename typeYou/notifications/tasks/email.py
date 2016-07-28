import os
import requests

from notifications.models import EmailNotification
from .base import SendNotificationBaseTask


class SendEmailTask(SendNotificationBaseTask):

    def get_object(self, object_id):
        email = EmailNotification.objects.get(id=object_id)
        return email

    def get_api_base_url(self):
        api_base_url = os.environ.get('EMAIL_BASE_URL')
        return api_base_url

    def get_headers(self):
        headers = (
            'api',
            os.environ.get('EMAIL_API_KEY'),
        )
        return headers

    def get_data(self, object):
        data = {
            'from': object.sender,
            'to': object.receiver,
            'subject': 'Welcome to typeYou',
            'text': object.content,
        }
        return data

    def run(self, object_id):
        object = self.get_object(object_id)
        api_base_url = self.get_api_base_url()
        headers = self.get_headers()
        data = self.get_data(object)
        response = requests.post(
                api_base_url,
                auth=headers,
                data=data,
        )
