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
                sender='Mailgun Sandbox <postmaster@sandbox61f776c58f814b4a9e82c975f94dcee0.mailgun.org>',
                receiver=instance.email,
                content='Congratulations woojong, you just sent an email with Mailgun!  You are truly awesome!  You can see a record of this email in your logs: https://mailgun.com/cp/log .  You can send up to 300 emails/day from this sandbox server.  Next, you should add your own domain so you can send 10,000 emails/month for free.',
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
