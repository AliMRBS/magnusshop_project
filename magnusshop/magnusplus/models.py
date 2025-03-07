from django.db import models


class Package(models.Model):
    title = models.CharField(max_length=447)
    price = models.PositiveBigIntegerField()
    description = models.TextField(blank=True)
    days = models.PositiveSmallIntegerField()
    is_enable = models.BooleanField(default=True)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PackageAttribute(models.Model):
    Package = models.ForeignKey(Package, related_name='attributes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title