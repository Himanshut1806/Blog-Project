from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name
 
class Blog(models.Model):
    title = models.CharField(max_length=255, null=True)
    body = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="blogs") 
    last_modified = models.DateTimeField(auto_now=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="blogs", null=True)
    image = models.ImageField(upload_to='', null=True, blank=True) 
    
    def __str__(self):
        return self.title


