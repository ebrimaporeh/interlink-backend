# courses/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, Certificate
import secrets

@receiver(post_save, sender=Enrollment)
def generate_certificate_number(sender, instance, created, **kwargs):
    if instance.status == 'completed' and not instance.certificate_issued:
        # Generate unique certificate number
        certificate_number = f"IGC-{instance.id}-{secrets.token_hex(4).upper()}"
        instance.certificate_number = certificate_number
        instance.certificate_issued = True
        instance.save(update_fields=['certificate_number', 'certificate_issued'])
        
        # Create certificate record
        Certificate.objects.create(
            enrollment=instance,
            certificate_number=certificate_number
        )