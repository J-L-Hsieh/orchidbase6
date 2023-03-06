from django.conf.urls import url,include
from django.contrib import admin
from simple_page.views import *
#from rec_histone.views import main_algorithm,Info_download,Sum_download,example_download
urlpatterns = [
    url(r'^tools/',tools,name="tools"),
    url(r'^Phalaenopsis_2020/',Phalaenopsis_2020,name="Phalaenopsis_2020"),
    url(r'^Dendrobium_2020/',Dendrobium_2020,name="Dendrobium_2020"),
    url(r'^Apostasia_2020/',Apostasia_2020,name="Apostasia_2020"),
    url(r'^Vpompona_2020/',Vpompona_2020,name="Vpompona_2020"),
    url(r'^Vshenzhenica_2020/',Vshenzhenica_2020,name="Vshenzhenica_2020"),
    url(r'^Pguangdongensis_2020/',Pguangdongensis_2020,name="Pguangdongensis_2020"),
    url(r'^Pzijinensis_2020/',Pzijinensis_2020,name="Pzijinensis_2020"),
    url(r'^Ldiscolor_2020/',Ldiscolor_2020,name="Ldiscolor_2020"),
]
