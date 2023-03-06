from django.conf.urls import url,include
from django.contrib import admin
from transcriptome.views import *
#from rec_histone.views import main_algorithm,Info_download,Sum_download,example_download
urlpatterns = [
    url(r'^$',GeneExpression,name='GeneExpression'),
    url(r'ajax_parse/$',GeneExpression_data,name='GeneExpression_data'),
    url(r'ajax_parse2/$',GeneExpression_select_data,name='GeneExpression_select_data'),
    url(r'ajax_parse3/$',GeneExpression_search_data,name='GeneExpression_search_data'),
    url(r'ajax_parse4/$',select_plot_cluster,name='select_plot_cluster'),
    url(r'ajax_parse5/$',GeneExpression_key_word_data,name='GeneExpression_key_word_data'),
    url(r'ajax_parse6/$',select_expression,name='select_expression')
]
