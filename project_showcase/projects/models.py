from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    technologies = models.JSONField()
    live_demo_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title