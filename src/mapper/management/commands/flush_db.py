from django.core.management import BaseCommand
from mapper.models import Protein

class Command(BaseCommand):
    """
    TODO: docs
    """
    help = "Erase the contents of the databases!"

    def handle(self, *args, **options):
        Peptide.objects.all().delete()
