import random, string
from django.db import models

class ShortURL(models.Model):
    original_url = models.URLField(unique=True)
    short_key = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.short_key:
            self.short_key = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.original_url} -> {self.short_key}"
    


