import os
CAP_DIR = os.getcwd() +'\cap'

import sys
sys.path.append(CAP_DIR + '\PartsInfo') #Path to BuildInfo directory
from django.shortcuts import render
from BuildInfo import BuildInfo
# Create your views here.
BI = BuildInfo(CAP_DIR + '\datasets\cpu_clean.csv', CAP_DIR + '\datasets\gpu_clean.csv', CAP_DIR + '\datasets\memory_clean.csv', CAP_DIR + '\datasets\storage_clean.csv', CAP_DIR + '\datasets\motherboard_clean.csv')


def index(request):
    request.session['price'] = '500'
    price = int(request.session.get('price'))

    BI.set_base_info(price,"office")
    res = BI.get_cpu_recommendation()
    return render(request,'web/home.html',{'CPU1': res[0][0],'CPU1_model': res[0][1],'CPU2': res[1][0],'CPU2_model': res[1][1],'CPU3': res[2][0],'CPU3_model': res[2][1]})

def welcome(request):
    return render(request, 'web/welcomePage.html')

def Step2(request):
    return render(request,'web/Step2.html')

def Step3(request):
    return render(request,'web/Step3.html')
