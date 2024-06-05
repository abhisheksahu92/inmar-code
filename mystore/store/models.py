from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MetaData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} - {self.department} - {self.category} - {self.subcategory}"

class SKU(models.Model):
    sku = models.IntegerField()
    name = models.CharField(max_length=255)
    metadata = models.ForeignKey(MetaData, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
