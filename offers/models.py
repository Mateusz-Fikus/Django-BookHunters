from django.db import models
from django.db.models.fields import BooleanField
from users.models import User

GENRE_CHOICES= [
    ('scifi', 'Sci-Fi'),
    ('fantasy', 'Fantasy'),
    ('action', 'Action'),
    ('comic', 'Comic'),
    ('historical', 'Historical'),
    ('adventure', 'Adventure'),
    ('romance', 'Romance'),
    ('horror', 'Horror'),
    ('biography', 'Biography'),
    ('other', 'Other')
    ]

class offer(models.Model):
    id_owner_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='seller')
    title = models.CharField(max_length=30)
    desc = models.TextField()
    price = models.IntegerField(null=False, blank=False)
    id_buyer = models.ForeignKey(User, null=True, blank=True, default=None, on_delete = models.CASCADE, related_name='buyer')
    front_picture = models.ImageField(upload_to='book_covers')
    genre = models.CharField(max_length=10, null=False, blank=False, choices=GENRE_CHOICES, default='other')
    
    def __str__(self):
        return self.title

#REQUESTS VISIBLE FOR SELLER
class pending(models.Model):
    id_offer = models.ForeignKey(offer, on_delete=models.CASCADE, related_name='offer_number')
    id_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selling_user')
    id_intrested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interested_user')
    message = models.CharField(max_length=250, default=None, blank=True)