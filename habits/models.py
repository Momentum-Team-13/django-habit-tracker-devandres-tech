from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Habit(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    target = models.IntegerField()

    def __str__(self):
        return self.name


class Record(BaseModel):
    date = models.DateField(blank=True, null=True, auto_now_add=True)
    daily_number = models.IntegerField()
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['habit', 'date'], name='unique_record')
        ]
