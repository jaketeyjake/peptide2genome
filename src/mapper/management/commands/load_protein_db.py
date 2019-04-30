from django.core.management import BaseCommand
from peptide2genome.utils.db import fasta_parse
from mapper.models import Protein


class Command(BaseCommand):
    """
    TODO: docs
    """
    help = "Load up the protein database into sqlite db"

    db_location = "./data/Homo_sapiens.GRCh38.pep.all.fa"

    def handle(self, *args, **options):
        protein_data = fasta_parse(self.db_location, all_records=False)
        protein_data.apply(self._protein_db_helper, axis=1)

    @staticmethod
    def _protein_db_helper(x):
        Protein.objects.create(accession=x.accession, sequence=x.sequence)
