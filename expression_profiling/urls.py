from django.conf.urls import url,include
from django.contrib import admin
from expression_profiling.views import *

urlpatterns = [
    url(r'BLAST_SCA/$',BLAST_SCA,name='BLAST_SCA'),
    url(r'BLAST_PEP/$',BLAST_PEP,name='BLAST_PEP'),
    url(r'ajax_parse/$',Run_BLAST_SCA,name='Run_BLAST_SCA'),
    url(r'ajax_parse2/$',Run_BLAST_PEP,name='Run_BLAST_PEP'),
    url(r'ajax_parse3/$',expression,name='expression'),
    url(r'ajax_parse4/$',select_expression,name='select_expression'),
    url(r'ajax_parse5/$',select_plot_cluster,name='select_plot_cluster'),
]
