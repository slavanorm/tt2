from image_handler import settings
from image_handler.models import ImageModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


@receiver(post_save, sender=ImageModel)
def update_file_path(instance, created, **kwargs):
    if created:
        path0 = instance.file.path

        dir = settings.MEDIA_ROOT
        ext = os.path.splitext(path0)[1]

        path1 = str(instance.pk) + ext
        os.rename(path0,
                  os.path.join(
                      dir,path1))
        instance.file = path1
        instance.save()