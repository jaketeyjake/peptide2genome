from django.core.management import BaseCommand
from mapper.models import Peptide, SpanGroup, Region, SpanGroup_Regions, Peptide_SpanGroups

class Command(BaseCommand):
    """
    TODO: docs
    """
    help = "Erase the contents of all databases except Protein!"

    def handle(self, *args, **options):
        Peptide.objects.all().delete()
        SpanGroup.objects.all().delete()
        Region.objects.all().delete()
        SpanGroup_Regions.objects.all().delete()
        Peptide_SpanGroups.objects.all().delete()
