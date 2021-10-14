from django.db import models

class ImageModel(models.Model):
    """
    part of tech task is to have filename as {id}.jpg
    this is done with signal on post_save

    could also implement hashing and check if file exists
    """

    file = models.ImageField(blank=False)
