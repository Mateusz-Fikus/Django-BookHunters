from django.db import models

from users.models import User

# Create your models here.

class offer(models.Model):
    id_owner_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='seller')
    title = models.CharField(max_length=30)
    desc = models.TextField()
    location = models.CharField(max_length=30)
    id_buer = models.ForeignKey(User, null=True, blank=True, default=None, on_delete = models.CASCADE, related_name='buyer')



    def __str__(self):
        return self.title
