from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

# Create your models here.
class Route(models.Model):
    original_url = models.URLField(help_text= "Add the original URL that you want to shorten.")
    key = models.TextField(unique= True, help_text= "Add any random characters of your choice to shorten it.", blank=True )

    def __str__(self):
        return f"{self.original_url}"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_unique_key()
        super().save(*args, **kwargs)

    def generate_unique_key(self):
        while True:
            key = get_random_string(length=6)
            if not Route.objects.filter(key=key).exists():
                return key
            
    def get_absolute_url(self):
        return reverse('redirector', args=[self.key])