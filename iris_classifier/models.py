from django.db import models

class Collector(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    field_of_expertise = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)

class Iris(models.Model):
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    species = models.CharField(max_length=30)
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE)


    
