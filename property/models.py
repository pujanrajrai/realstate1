from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from accounts.models import MyUser


class PropertyCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class PropertyStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='property')
    category = models.ForeignKey(PropertyCategory, on_delete=models.PROTECT)
    status = models.ForeignKey(PropertyStatus, on_delete=models.PROTECT)
    location_state = models.ForeignKey(State, models.PROTECT)
    location = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    desc = RichTextField()
    added_date = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    total_click = models.IntegerField(default=0, blank=True, null=True)
    is_price_negotiable = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# user = models.ForeignKey(MyUser, on_delete=models.PROTECT),
#     property = models.ForeignKey(Property, on_delete=models.PROTECT),
#     date_of_added = models.DateTimeField(auto_now=True)


class PropertyBookMark(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    is_vist_req = models.BooleanField(default=False)


    class Meta:
        unique_together = ['user', 'property']


class Comments(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    date_of_added = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=1000)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.comment
