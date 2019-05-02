from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from .models import Protein, Peptide, SpanGroup, Region, Peptide_SpanGroups, SpanGroup_Regions
from .serializers import ProteinSerializer, PeptideSerializer, SpanGroupSerializer, RegionSerializer
from .serializers import Peptide_SpanGroupsSerializer, SpanGroup_RegionsSerializer


# Create your views here.
class ProteinViewSet(ModelViewSet):
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer


class PeptideViewSet(ModelViewSet):
    queryset = Peptide.objects.all()
    serializer_class = PeptideSerializer


class SpanGroupViewSet(ModelViewSet):
    queryset = SpanGroup.objects.all()
    serializer_class = SpanGroupSerializer


class RegionViewSet(ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class Peptide_SpanGroupsViewSet(ModelViewSet):
    queryset = Peptide_SpanGroups.objects.all()
    serializer_class = Peptide_SpanGroupsSerializer


class SpanGroup_RegionsViewSet(ModelViewSet):
    queryset = SpanGroup_Regions.objects.all()
    serializer_class = SpanGroup_RegionsSerializer
