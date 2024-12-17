from django.db import models

# Create your models here.

class Topic(models.Model):
    """the topic that user learning."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return models' string presentation."""
        return self.text

class Entry(models.Model):
    """detailed knowledge about some topics"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """return model's string presentation"""
        return f"{self.text[:50]}..."
