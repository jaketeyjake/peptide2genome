from django.forms import Form, CharField, ModelForm
from .models import Peptide


class PeptideReqsForm(Form):
    peptide = CharField(label="Peptide Sequence", max_length=64)


class PeptideForm(ModelForm):

    class Meta:
        model = Peptide
        fields = ('sequence',)

