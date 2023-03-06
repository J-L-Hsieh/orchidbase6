from django.conf.urls import url,include
from django.contrib import admin
from home.views import *
#from rec_histone.views import main_algorithm,Info_download,Sum_download,example_download
urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'^rec_histone/$',main_algorithm,name="main_algorithm"),
    #url(r'Info_download/$',Info_download,name="Info_download"),
    #url(r'Sum_download/$',Sum_download,name="Sum_download"),
    #url(r'example_download/$',example_download,name="example_download"),
    url(r'^$',home,name='home'),
    #url(r'ajax_parse/$',GeneExpression_data,name='GeneExpression_data')
]
