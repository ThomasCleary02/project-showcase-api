from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)  # Fixed typo: 225 -> 255
    subtitle = models.CharField(max_length=255, blank=True)  # Made optional
    url = models.URLField(unique=True)  # Added unique constraint
    img_url = models.URLField(blank=True)  # Made optional
    published_date = models.DateField(null=True, blank=True)  # Added publication date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Added update timestamp

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title