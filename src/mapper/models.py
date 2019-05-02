from django.db import models


class Protein(models.Model):
    accession = models.CharField(max_length=20, primary_key=True)
    sequence = models.TextField()


class Peptide(models.Model):
    sequence = models.CharField(max_length=64, primary_key=True)
    requests = models.IntegerField()


class SpanGroup(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    chromosome = models.CharField(max_length=3)
    start = models.IntegerField()
    end = models.IntegerField()
    members = models.IntegerField()


class Region(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    chromosome = models.CharField(max_length=3)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.IntegerField()


class SpanGroup_Regions(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    span_group = models.ForeignKey(SpanGroup, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Peptide_SpanGroups(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    peptide = models.ForeignKey(Peptide, on_delete=models.CASCADE)
    span_group = models.ForeignKey(SpanGroup, on_delete=models.CASCADE)
