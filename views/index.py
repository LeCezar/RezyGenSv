from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView


class StartIndexView(TemplateView):
    template_name = "index.html"
