from django.contrib import admin
from .models import Protein, Peptide, SpanGroup, Region, SpanGroup_Regions, Peptide_SpanGroups

# Register your models here.

admin.site.register(Protein)
admin.site.register(Peptide)
admin.site.register(SpanGroup)
admin.site.register(Region)
admin.site.register(SpanGroup_Regions)
admin.site.register(Peptide_SpanGroups)
