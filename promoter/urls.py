from django.conf.urls import url,include
from django.contrib import admin
from promoter.views import *

urlpatterns = [
	url(r'^$',promoter_table,name='promoter_table'),
	url(r'^promoter_table_data/',promoter_table_data,name='promoter_table_data'),
    url(r'^promoter_detail/',promoter,name='promoter_detail'),
    url(r'^sequence_result/',sequence_result,name='sequence_result'),
    url(r'^click_result/',click_result,name='click_result'),
    #url(r'sequence_result/$',sequence_result,name='sequence_result'),#$為HMMER/ajax_hmmer/，最終變為140.116.214.130/t50504_project/HMMER/HMMER/ajax_hmmer
    #url(r'^ajax_similar_gene/',similar_gene,name='similar_gene'),
]
