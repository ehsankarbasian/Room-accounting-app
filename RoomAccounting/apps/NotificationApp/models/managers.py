from django.contrib.contenttypes.models import ContentType
from django.db import models


class NotificationChannelQuerySet(models.QuerySet):

    def for_recipient(self, recipient):
        recipient_content_type = ContentType.objects.get_for_model(recipient)

        return self.filter(
            recipient_content_type=recipient_content_type,
            recipient_object_id=recipient.id,
        )
