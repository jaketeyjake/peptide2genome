from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from .models import Protein, Peptide, SpanGroup, Region, Peptide_SpanGroups, SpanGroup_Regions
from .serializers import ProteinSerializer, PeptideSerializer, SpanGroupSerializer, RegionSerializer
from .serializers import Peptide_SpanGroupsSerializer, SpanGroup_RegionsSerializer
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import PeptideReqsForm, PeptideForm
from django.db.models import F
import logging

logger = logging.getLogger('VIEWS')
logger.setLevel(logging.DEBUG)
console_logger = logging.StreamHandler()
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_logger.setFormatter(console_format)
logger.addHandler(console_logger)

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


def peptide_list(request):
    # static call for now, request will be fed by form
    # will need to inspect request.cleaned_data or something
    logger.info('Entered peptide_list')

    if request.method == 'POST':
        logger.info('Data has been posted' + str(request.POST))
        form = PeptideForm(request.POST)
        # print(form)
        search_token = request.POST['sequence']
        logger.info('Search token is:' + search_token)
        peptides = Peptide.objects.filter(sequence=search_token)
        if not peptides.exists():
            # TODO: peptide registration function
            # peptides =
            pass
        else:
            # increment the counter
            peptides.update(requests=F('requests') + 1)
    else:
        # Just return the and example peptide if nothing is posted
        example_peptide = 'ARTKQTARKS'
        peptides = Peptide.objects.filter(sequence=example_peptide)

    span_group_ids_for_peptide = Peptide_SpanGroups.objects.filter(peptide=peptides.get())
    span_group_data = SpanGroup.objects.filter(id__in=span_group_ids_for_peptide.values('span_group')).order_by(
        'chromosome', 'start'
    )
    # logger.info(span_group_data)

    return render(request, 'peptide_list/index.html', {'peptides': peptides, 'spangroups': span_group_data})
    # return render(request, 'peptide_list/index.html', {'peptides': peptides})


def peptide_search(request):
    form = PeptideForm()
    return render(request, 'peptide_list/peptide_search.html', {'form': form})


def get_pep_requests(request):

    if request.method == 'POST':
        form = PeptideReqsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/pepreqdisp/')

    else:
        form = PeptideReqsForm()

    return render(request, 'peptide_search.html', {'form': form})
