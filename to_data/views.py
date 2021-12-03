from django.views import generic
from django.shortcuts import render
from .forms import FileUpload
from .forms import SelectColumns
from . import variable as var
import csv,io
import pandas as pd

class IndexView(generic.FormView):
    template_name = 'index.html'
    form_class = FileUpload

    def form_valid(self, form):
        if 'upload' in self.request.POST:
            # カテゴリーに対応するDATASETを呼び出す
            select_form = SelectColumns()
            select_form.fields['columns'].choices = var.DATASET[form.cleaned_data['category']]
            select_form.fields['columns'].initial = ['都道府県コード又は市区町村コード']

            # "ThisComputer"のとき
            if form.cleaned_data['file']:
                df = pd.read_csv(io.StringIO(self.request.FILES['file'].read().decode('utf-8')), delimiter=',')
                col = df.columns.values
                context = {
                    'category': form.cleaned_data['category'],
                    'col': col,
                    'file': df.to_html(),
                    'form': select_form
                }
                return render(self.request, 'processing.html', context)

            # "Web Addressed(URLs)"のとき
            elif form.cleaned_data['url']:
                df = pd.read_csv(self.request.POST['url'])
                col = df.columns.values
                context = {
                    'category': form.cleaned_data['category'],
                    'col': col,
                    'file': df.to_html(),
                    'form': select_form
                }
                return render(self.request, 'processing.html', context)

