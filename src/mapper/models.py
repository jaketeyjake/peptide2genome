from django.db import models


class Protein(models.Model):
    accession = models.CharField(max_length=20, primary_key=True)
    sequence = models.TextField()

