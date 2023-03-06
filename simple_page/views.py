from django.shortcuts import render,render_to_response
from django.views.decorators import csrf
import os,datetime
import pandas as pd
import time
import sys
from django.http import HttpResponse,JsonResponse
import collections


def tools(request):
	return render(request,'tools.html',locals())

def Phalaenopsis_2020(request):
	return render(request,'Phalaenopsis_2020.html',locals())

def Dendrobium_2020(request):
	return render(request,'Dendrobium_2020.html',locals())

def Apostasia_2020(request):
	return render(request,'Apostasia_2020.html',locals())

def Vpompona_2020(request):
	return render(request,'Vpompona_2020.html',locals())
	
def Vshenzhenica_2020(request):
	return render(request,'Vshenzhenica_2020.html',locals())

def Pguangdongensis_2020(request):
	return render(request,'Pguangdongensis_2020.html',locals())

def Pzijinensis_2020(request):
	return render(request,'Pzijinensis_2020.html',locals())

def Ldiscolor_2020(request):
	return render(request,'Ldiscolor_2020.html',locals())
