from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Update
from .views import send_notifications_to_all  # Import your notification function

@receiver(post_save, sender=Update)
def send_notification_on_update_save(sender, instance, created, **kwargs):
    if created:  # Only send notifications when a new Update is created
        print("Signal triggered for update creation.")
        message_body = f"New Update: {instance.title}\n{instance.content}"
        send_notifications_to_all(message_body)
