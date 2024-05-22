from django.db import models

class DataFile(models.Model):
  file = models.FileField(upload_to='uploads/')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"File: {self.file.name}"
