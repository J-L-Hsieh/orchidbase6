from django.conf.urls import url,include
from django.contrib import admin
from pfam.views import *

urlpatterns = [
    url(r'^$',hmmer,name='hmmer'),
    url(r'^ajax_hmmer/',Ajax_func,name='ajax_func'),
    url(r'^ajax_interproscan/',Interproscan,name='Interproscan'),
    #url(r'ajax_hmmer/$',Ajax_func,name='ajax_func'),#$為HMMER/ajax_hmmer/，最終變為140.116.214.130/t50504_project/HMMER/HMMER/ajax_hmmer
    url(r'^ajax_similar_gene/',similar_gene,name='similar_gene'),
    url(r'^ajax_similar_gene_interproscan/',similar_gene_interproscan,name='similar_gene_interproscan'),
    url(r'^GeneExpressionProfile/',GeneExpressionProfile,name="GeneExpressionProfile"),
    url(r'^select_expression/',select_expression,name="select_expression"),
    url(r'^download/',file_download,name="download"),
    url(r'^select_plot_cluster/',select_plot_cluster,name="select_plot_cluster"),
    url(r'^query_ID_Pfam/',query_ID_Pfam,name="query_ID_Pfam"),
    url(r'^query_ID_interproscan/',query_ID_interproscan,name="query_ID_interproscan"),
    url(r'^query_keyword_Pfam/',query_keyword_Pfam,name="query_keyword_Pfam"),
    url(r'^query_keyword_interproscan/',query_keyword_interproscan,name="query_keyword_interproscan"),
]