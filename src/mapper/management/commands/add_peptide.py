from django.core.management import BaseCommand
from peptide2genome.utils.db import fasta_parse
from mapper.models import Protein, Peptide, SpanGroup, Region, SpanGroup_Regions, Peptide_SpanGroups
import re
import requests
import hashlib
import pandas as pd
import logging

logger = logging.getLogger('AddPeptide')
logger.setLevel(logging.DEBUG)
console_logger = logging.StreamHandler()
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_logger.setFormatter(console_format)
logger.addHandler(console_logger)


class Command(BaseCommand):
    """
    TODO: docs
    """
    help = "Load up the protein database into sqlite db"

    base_url = 'https://rest.ensembl.org/map/translation/'
    url_suffix = '?content-type=application/json'
    hash_length = 10
    LIVE = True

    def add_arguments(self, parser):
        parser.add_argument('peptide', type=str)

    def handle(self, *args, **options):
        logger.info('Handling add_peptide command for:')
        logger.info(options['peptide'])

        peptide = options['peptide']
        peptide_length = len(peptide)

        # check if peptide exists already in db, if so, return, else:

        check_for_peptide = Peptide.objects.filter(sequence=peptide)

        if check_for_peptide.exists():
            logger.info(peptide + ' was found.')
            return
        else:
            logger.info(peptide + ' was not found. Creating!')

        proteins_with_peptide = Protein.objects.filter(sequence__contains=peptide)

        logger.info('Entries containing the peptide: ' + str(len(proteins_with_peptide)))

        if len(proteins_with_peptide) > 0:

            # create the peptide and set its request to 1
            if self.LIVE:
                logger.info("Creating Peptide: " + peptide)
                po = Peptide.objects.create(sequence=peptide, requests=1)
            else:
                logger.info("IF LIVE: Would have created Peptide: " + peptide)

            # find the peptide in proteins in the database
            for result in proteins_with_peptide:
                match_start = []
                accession = result.accession
                accession_parts = accession.split('.')
                accession_trimmed = accession_parts[0]
                logger.info('Accession:' + accession_trimmed)
                pattern = re.compile(peptide)

                for match in pattern.finditer(result.sequence):
                    match_start.append(match.start())
                    logger.info('  -match at: ' + str(match.start()))

                logger.info(len(match_start))

                for match_pos in match_start:
                    formulated_url = self.base_url + accession_trimmed + "/" + str(match_pos+1) + ".." + str(match_pos+peptide_length) + self.url_suffix
                    logger.info(formulated_url)
                    response = requests.get(formulated_url)
                    decoded = response.json()
                    logger.info(decoded)

                    response_table = pd.DataFrame(data=decoded['mappings'])

                    spangroup_absolute_start = response_table['start'].min()
                    spangroup_absolute_end = response_table['end'].max()
                    spangroup_n_segments = response_table.shape[0]
                    spangroup_chromosome = response_table.loc[0]['seq_region_name']

                    hashes = response_table.apply(self._create_hash_from_column_values,
                                                  args=('start', 'end', 'seq_region_name', 'strand'),
                                                  axis=1
                                                  )
                    response_table['id'] = hashes
                    response_table = response_table.sort_values(by=['id'])
                    logger.info(response_table)

                    spangroup_id = self._create_hash_from_list_of_ids(response_table['id'])
                    logger.info(spangroup_id)

                    # check if spangroup exists, if so, do nothing, else procede to checking regions

                    sg_query = SpanGroup.objects.filter(id=spangroup_id)

                    if sg_query.exists():
                        logger.info('This spangroup " + spangroup_id + " exists - do nothing')
                        continue

                    # Spangroup does not exist, continue

                    if self.LIVE:
                        sg_object = SpanGroup.objects.create(
                            id=spangroup_id,
                            chromosome=spangroup_chromosome,
                            start=spangroup_absolute_start,
                            end=spangroup_absolute_end,
                            members=spangroup_n_segments
                        )
                    else:
                        logger.info("IF LIVE: Would have created SpanGroup: " + spangroup_id)

                    regions = response_table.apply(self._get_id_or_create_region, axis=1)
                    print(regions)

                    # at this point the span group is created and all its regions are created/exist
                    # time to associate regions with the span group
                    if self.LIVE:
                        logger.info("Associating Regions to SpanGroup: " + spangroup_id)
                        for region_id in regions:
                            logger.info(region_id)
                            catenated_ids = spangroup_id + region_id
                            spangroup_to_region_id = self._do_hash(catenated_ids)
                            SpanGroup_Regions.objects.create(
                                id=spangroup_to_region_id,
                                span_group=SpanGroup.objects.get(id=spangroup_id),
                                region=Region.objects.get(id=region_id)
                            )
                    else:
                        logger.info("IF LIVE: Would have associated Regions to SpanGroup: " + spangroup_id)

                    # now also associate peptide with spangroup
                    peptide_spangroup_catenated_ids = peptide + spangroup_id
                    peptide_spangroup_id = self._do_hash(peptide_spangroup_catenated_ids)

                    if self.LIVE:
                        logger.info(
                            "Associating SpanGroup: " + spangroup_id + " to Peptide: " + peptide
                        )
                        Peptide_SpanGroups.objects.create(
                            id=self._do_hash(peptide_spangroup_catenated_ids),
                            peptide=Peptide.objects.get(sequence=peptide),
                            span_group=SpanGroup.objects.get(id=spangroup_id)
                        )
                    else:
                        logger.info(
                            "IF LIVE: Would have associated SpanGroup: " + spangroup_id + " to Peptide: " + peptide
                        )

                    # iterate through decoded.mappings


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
            logger.info('That peptide does not exist in the master database...doing nothing')

    def _create_hash_from_column_values(self, x, *args):
        """
        Create a hash representation of certain fields in a pandas df
        :param x:
        :param args:
        :return:
        """
        data_string = ''
        for colname in args:
            data_string += str(x[colname])
        print(data_string)
        return self._do_hash(data_string)

    def _get_id_or_create_region(self, x):
        region_id_query = Region.objects.filter(id=x['id'])
        if region_id_query.exists():
            pass
        else:
            if self.LIVE:
                logger.info("Creating Region: " + x['id'])
                Region.objects.create(
                    id=x['id'],
                    start=x['start'],
                    end=x['end'],
                    chromosome=x['seq_region_name'],
                    strand=x['strand']
                )
            else:
                logger.info("IF LIVE: Would have created Region: " + x['id'])

        return x['id']

    def _create_hash_from_list_of_ids(self, idlist):
        data_string = "".join(idlist)
        return self._do_hash(data_string)

    def _do_hash(self, data_string):
        hasher = hashlib.sha256()
        encoded_data_string = data_string.encode()
        hasher.update(encoded_data_string)
        return hasher.digest().hex()[0:self.hash_length]
