from django.db import models

from users.models import User

# Create your models here.

class offer(models.Model):
    id_owner_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='seller')
    title = models.CharField(max_length=30)
    desc = models.TextField()
    price = models.SmallIntegerField(null=False, blank=False)
    id_buer = models.ForeignKey(User, null=True, blank=True, default=None, on_delete = models.CASCADE, related_name='buyer')
    front_picture = models.ImageField(upload_to='book_covers')
    back_picture = models.ImageField(upload_to='book_covers', null='True', blank=True, default=None)
    genre = models.CharField(max_length=10, null=False, blank=False)
    
    def __str__(self):
        return self.title


