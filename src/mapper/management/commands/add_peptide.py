from django.core.management import BaseCommand
from peptide2genome.utils.db import fasta_parse
from mapper.models import Protein, Peptide, SpanGroup, Region, SpanGroup_Regions, Peptide_SpanGroups
import re
import requests
import hashlib


class Command(BaseCommand):
    """
    TODO: docs
    """
    help = "Load up the protein database into sqlite db"

    base_url = 'https://rest.ensembl.org/map/translation/'
    url_suffix = '?content-type=application/json'
    hash_length = 10
    hasher = hashlib.sha256()

    def add_arguments(self, parser):
        parser.add_argument('peptide', type=str)

    def handle(self, *args, **options):
        print(options['peptide'])

        peptide = options['peptide']
        peptide_length = len(peptide)

        # check if peptide exists already in db, if so, return, else:

        check_for_peptide = Peptide.objects.filter(sequence=peptide)

        if check_for_peptide.exists():
            print(peptide + ' was found.')
            return
        else:
            print(peptide + ' was not found. Creating!')

        proteins_with_peptide = Protein.objects.filter(sequence__contains=peptide)
        if len(proteins_with_peptide) > 0:

            # create the peptide and set its request to 1
            # po = Peptide.objects.create(sequence=peptide, requests=1)

            # find the peptide in proteins in the database
            for result in proteins_with_peptide:
                match_start = []
                accession = result.accession
                accession_parts = accession.split('.')
                accession_trimmed = accession_parts[0]
                print('Accession:' + accession_trimmed)
                pattern = re.compile(peptide)

                for match in pattern.finditer(result.sequence):
                    match_start.append(match.start())
                    print('  -match at: ' + str(match.start()))

                print(len(match_start))

                for match_pos in match_start:
                    formulated_url = self.base_url + accession_trimmed + "/" + str(match_pos+1) + ".." + str(match_pos+peptide_length) + self.url_suffix
                    print(formulated_url)
                    response = requests.get(formulated_url)
                    decoded = response.json()
                    print(decoded)

                    # iterate through decoded.mappings
                    absolute_start = 0
                    absolute_end = 0
                    span_group_data_to_hash = ''
                    for segment in decoded['mappings']:
                        pass
                        # gather info: start, end, chromosome, strand
                        hashable_representation = \
                            str(
                                segment['start']) + str(
                                segment['end']) + str(
                                segment['seq_region_name']) + str(
                                segment['strand']
                            )

                        hashable_representation = hashable_representation.encode()
                        self.hasher.update(hashable_representation)
                        segment_id = self.hasher.digest().hex()[0:self.hash_length]

                        # hash the data, pile on to data_string_to_hash

                        # check if it already exists based on hash, if not add

                        # collect the region ids just in case a new SpanGroup is created

                    # hash the span group data

                    # check if it exists, if not add

                    # if a new span group was added, we need to update the SpanGroup_Regions table
                    # the id would be a hash of the combined hashes of every SpanGroup - Region id combination
                    # also, collect the new span group id so we can associate it with the peptide

            # check if new span groups were created, if so, associate to peptides
            # create a new Peptide-SpanGroup ID based on a hash of the combined ids of every Peptide and SpanGroup

        else:
            print('That peptide does not exist in the database')
