from django.shortcuts import render,render_to_response
from django.views.decorators import csrf
import os,datetime
import pandas as pd
import time
import sys
from django.http import HttpResponse,JsonResponse
import collections
# Create your views here.
def home(request):
    #print("I am a handsome boy")
    return render(request,'home.html',locals()) #locals()用來組成字典傳遞變數給模板