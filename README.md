# peptide2genome
Proteomics application to map tryptic peptides to human genome

### Background:
peptide2genome is a Django-backed web application to map short segments
of proteins (up to 64 amino acids) to genomic coordinates.  It uses RESTful
services from Ensembl to assist with this mapping, but then allows for
extremely fast lookup of peptides and request tracking.  Ultimately,
this framework will allow for large-scale mapping of proteomic data sets
so that they can be made more compatible with RNA-Seq data for integrative
analyses.  It also gracefully handles the redundancy often present in genomic
data and the bioinformatic resources derived from them.

### Under the hood:
Upon receiving a request to map a peptide sequence, peptide2genome
will first check to see if it has been requested previously.  If so, 
the mapping data should be returned almost instantly.  The application 
will return two types of information:
1) How many times has this peptide been requested to be mapped (incremented by this request)
2) The genomic location(s) for all instances of the peptide

If the peptide has never been requested before, the following steps occur:
1) Retrieve all instances of the peptide present the protein database
2) Retrieve all genomic coordinates of these instances using the Ensembl
REST API
3) For each coordinate group, create database entries for the coarse (SpanGroups)
 and fine mapping (Regions) of the peptide.
4) Associate Regions to SpanGroups and SpanGroups to Peptides in the
relational database

These steps may take some time (~seconds to minutes) depending on the degree of redundancy for this peptide 
in the initial protein database.  Remember that it relies on REST API calls to 
an external resource.

#### Implementation note:
Behind the scenes, peptide2genome represents IDs of most database entries as
sha256 hash representations of the rest of their contents.  This deterministic
 id formulation convention is used to make sure that no duplicate work 
 is ever performed during the mapping process.  If a SpanGroup or Region already exists
 there is no need to recreate it, even though they might be reused repeatedly in the
 association tables.  Hash representations of contents make it easier to manage
 *many-to-many* relationships that may exist in real bioinformatic scenarios.

###Getting started:
Clone or fork this repository.  You will also want to download the complete
database of Ensembl proteins that correspond to the current release of the
human genome
(ftp://ftp.ensembl.org/pub/release-96/fasta/homo_sapiens/pep/Homo_sapiens.GRCh38.pep.all.fa.gz).

This project uses [pipenv](https://docs.pipenv.org/en/latest/) to manage 
environment and dependencies.  You will need to install pipenv and also
need to create / export one environment variable before running this
project:

    DATABASE_URL=sqlite:///data/db.sqlite

Simply create .env in the root of the project folder and add this line to it.

Once that's done, you can issue this command:
    
    pipenv install

### Protein database prep:
We need to prepopulate our database with the protein data that you downloaded
from Ensembl.  Unzip this file and place it in the `data/` directory off the
root of the repository.  It should be called `Homo_sapiens.GRCh38.pep.all.fa`.
Then, run a Django management command to prepopulate the protein database:

    pipenv run python manage.py load_protein
   
 This may take a few minutes.  It uses Biopython in the background to
 read these sequences and Django ORM to populate the database.
 
 ### Running the application
 Now you should be all set to go.  Issue the following command:
 
     pipenv run python manage.py runserver
     
Go ahead and point your browser to http://127.0.0.1:8000/peptide2genome/peptide_search. 
Enter any arbitrary peptide sequence (up to 64 letters, no spaces) and hit
the **Find it!** button.  As long as it is in the protein database it will
be mapped.
 

