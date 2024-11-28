from django.db import models

# Create your models here.
class Player(models.Model):
        name = models.CharField(max_length=15)
        score = models.IntegerField()

        def __str__(self):
                return f'{self.name}: {self.score}'

class Tile(models.Model):
    tag = models.CharField(max_length=1)
    row = models.IntegerField()
    col = models.IntegerField()

    def __str__(self):
        return f'{self.tag} @({self.row}, {self.col})'