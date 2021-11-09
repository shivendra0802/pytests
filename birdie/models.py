from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.TextField()

    def get_excerpt(self, chars):
        return self.title[:chars]
