from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

# Link Scraper model


class Link(models.Model):
    address = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

# Banner ad for Link Scraper Tool


class WhosBanner(models.Model):
    image = models.ImageField(default='banner.png', upload_to='banner/')

    def __str__(self):
        return f"Banner: {self.image.name}"

# Delete banner image url path when admin delete image


@receiver(pre_delete, sender=WhosBanner)
def delete_image(sender, instance, **kwargs):
    # Delete the image file when the instance is deleted
    # Passing False avoids saving the model again
    instance.image.delete(False)


# Register the signal
pre_delete.connect(delete_image, sender=WhosBanner)

# Banner ad for Link Scraper Tool


class ScraperBanner(models.Model):
    image = models.ImageField(default='banner.png', upload_to='banner/')

    def __str__(self):
        return f"Banner: {self.image.name}"

# Delete banner image url path when admin delete image


@receiver(pre_delete, sender=ScraperBanner)
def delete_image(sender, instance, **kwargs):
    # Delete the image file when the instance is deleted
    # Passing False avoids saving the model again
    instance.image.delete(False)


# Register the signal
pre_delete.connect(delete_image, sender=ScraperBanner)
