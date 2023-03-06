
from django.conf.urls import url,include
from django.contrib import admin
from GeneAnnotation.views import *
urlpatterns = [
    url(r'^$',GeneAnnotation,name='GeneAnnotation'),
    url(r'GeneID_detail/$',GeneID_detail,name='GeneID_detail'),
    url(r'ajax_parse/$',GeneAnnotation_data,name='GeneAnnotation_data'),
    url(r'ajax_parse2/$',GeneAnnotation_select_data,name='GeneAnnotation_select_data'),
    url(r'ViewPathway/$',ViewPathway,name='ViewPathway'),   
    url(r'ajax_parse3/$',ViewPathway_data,name='ViewPathway_data'),
    url(r'ViewGoTerm/$',ViewGoTerm,name='ViewGoTerm'),
    url(r'ajax_parse4/$',ViewGoTerm_data,name='ViewGoTerm_data'),
    url(r'ViewInterPro/$',ViewInterPro,name='ViewInterPro'),
    url(r'ajax_parse5/$',ViewInterPro_data,name='ViewInterPro_data'),       
    #url(r'(?P<pk>[_\w]+/$)',GeneID_detail,name="GeneID_detail")#[_\w]+為正則表達式
]
