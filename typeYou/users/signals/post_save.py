import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission

from users.models import Teacher, Student, VerificationCode
from notifications.models import SMSNotification, EmailNotification

from hashids import Hashids


@receiver(post_save, sender=VerificationCode)
def post_save_verification(sender, instance, created, **kwargs):
    if created:
        hashids = Hashids(salt="create verification code", min_length=6)
        instance.hash_id = hashids.encode(instance.id)
        instance.save()

        sms = SMSNotification.objects.create(
                sender='01031186228',
                receiver=instance.phonenumber,
                content='Verification Code: {code}'.format(
                    code=instance.hash_id,
                ),
        )


@receiver(post_save, sender=Teacher)
def post_save_teacher(sender, instance, created, **kwargs):
    if created:
        permission = Permission.objects.get(codename='is_teacher')
        permission1 = Permission.objects.get(codename='create_question')
        instance.user_permissions.add(
                permission,
                permission1,
        )
        sms = SMSNotification.objects.create(
                sender='01031186228',
                receiver=instance.phonenumber,
                content='Thank you for registering as a Teacher',
        )
        email = EmailNotification.objects.create(
                sender=os.environ.get('EMAIL_SENDER'),
                receiver=instance.email,
                content=os.environ.get('EMAIL_CONTENT'),
        )
        instance.save()


@receiver(post_save, sender=Student)
def post_save_student(sender, instance, created, **kwargs):
    if created:
        permission = Permission.objects.get(codename='is_student')
        instance.user_permissions.add(
                permission,
        )
        sms = SMSNotification.objects.create(
                sender='01031186228',
                receiver=instance.phonenumber,
                content='Thank you for registering as a Student',
        )
        instance.save()
