# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    arquivo = forms.FileField(
        label='Escolha um arquivo(pdf):',
    )
