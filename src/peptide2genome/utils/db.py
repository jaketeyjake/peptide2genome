from Bio import SeqIO
import pandas as pd
import re
import hashlib

ensembl_locator_field_position = 2
chromosome_locator_field_position = 2
reasonable_chromosome_name_length = 2
reasonable_protein_length = 6
default_db_name = "data/Homo_sapiens.GRCh38.pep.all.fa"
reasonable_peptide_length = 6
trypsin_pattern = r'[A-Z]*?[KR](?!P)|[A-Z]+?$|[A-Z]+?(?=\*)'
hash_length = 10


def fasta_parse(fasta_name=default_db_name, all_records=False):
    accessions = []
    sequences = []

    for record in SeqIO.parse(fasta_name, "fasta"):
        if not all_records:
            locator_field = record.description.split()[ensembl_locator_field_position]
            chromosome_name = locator_field.split(":")[chromosome_locator_field_position]
            if len(chromosome_name) > reasonable_chromosome_name_length:
                continue
            if len(record.seq) < reasonable_protein_length:
                continue

        accessions.append(record.id)
        sequences.append(record.seq.__str__())

    entries = pd.DataFrame(data={'accession': accessions, 'sequence': sequences})

    return entries


def digest_entry(entry, pattern=trypsin_pattern):
    candidates = entry.sequence.findall(pattern=pattern)
    valid = pd.DataFrame(columns=['id', 'accession', 'sequence', 'start', 'end'])
    position_counter = 1
    hasher = hashlib.sha256()

    for c in candidates:
        if c.length > reasonable_peptide_length:
            start = position_counter
            end = position_counter + c.length - 1
            defining_string_bytes = str(entry.accession + c + str(start) + str(end)).encode()
            hasher.update(defining_string_bytes)
            id = hasher.digest().hex()[0:hash_length]
            valid = valid.append({'id': id, 'accession': entry.accession, 'sequence': c, 'start': start, 'end': end},
                                 ignore_index=True)

        position_counter = position_counter + c.length

    return valid
