from rest_framework.serializers import ModelSerializer, Serializer, IntegerField, FloatField
from mapper.models import Protein, Peptide, SpanGroup, Region, SpanGroup_Regions, Peptide_SpanGroups


class ProteinSerializer(ModelSerializer):
    class Meta:
        model = Protein
        fields = '__all__'


class PeptideSerializer(ModelSerializer):
    class Meta:
        model = Peptide
        fields = '__all__'


class SpanGroupSerializer(ModelSerializer):
    class Meta:
        model = SpanGroup
        fields = '__all__'


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class SpanGroup_RegionsSerializer(ModelSerializer):
    class Meta:
        model = SpanGroup_Regions
        fields = '__all__'


class Peptide_SpanGroupsSerializer(ModelSerializer):
    class Meta:
        model = Peptide_SpanGroups
        fields = '__all__'
