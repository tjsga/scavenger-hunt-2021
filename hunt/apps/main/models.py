from django.db import models
from django.db.models.fields.related import ManyToManyField


class Challenge(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    flag = models.CharField(max_length=50, null=False, blank=False)
    points = models.IntegerField(null=False, blank=False)
    exclusive = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

class Class(models.Model):
    YEAR_CHOICES = (('2022', 'Seniors'), ('2023', 'Juniors'), ('2024', 'Sophomores'), ('2025', 'Freshmen'))

    id = models.AutoField(primary_key=True, null=False, blank=False)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, null=False, blank=False, unique=True)
    challenges_completed = models.ManyToManyField(Challenge, related_name="classes_completed", blank=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.year

    def get_points(self):
        sum = 0
        for c in self.challenges_completed.all():
            sum += c.points
        return sum
    