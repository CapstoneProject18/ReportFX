import sys
import os
CAP_DIR = os.getcwd() +'/cap'

sys.path.append('/home/akshat/Desktop/ReportFX/cap/PartsInfo') #Path to BuildInfo directory
from django.shortcuts import render
from BuildInfo import BuildInfo
import CSVinfo as cs
import logging
from plotly.offline import plot
import plotly.graph_objs as go




logger = logging.getLogger(__name__)
# Create your views here.
baseURL = CAP_DIR + '/datasets/'

BI = BuildInfo(baseURL+'cpu_clean.csv',baseURL+'gpu_clean.csv',baseURL+'memory_clean.csv',baseURL+'storage_clean.csv',baseURL+'motherboard_clean.csv')
# request.session['price'] = '500'
# price = int(request.session.get('price'))
BI.set_base_info(1000, 'home')
CPU = 0
GPU= 0
RAM = 0
STORAGE = 0
def index(request):
    return render(request,'web/welcomePage.html')

def Step1(request):
        
    # request.session['price'] = '500'
    # price = int(request.session.get('price'))

    # BI.set_base_info(price,"office")
    res = BI.get_cpu_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][cs.CPU_PROCESSOR_NUMBER],res[1][cs.CPU_PROCESSOR_NUMBER],res[2][cs.CPU_PROCESSOR_NUMBER]],
            y=[res[0][cs.CPU_PERFORMANCE_SCORE],res[1][cs.CPU_PERFORMANCE_SCORE], res[2][cs.CPU_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/home.html',{'CPU1': res[0][0],'CPU1_model': res[0][cs.CPU_PROCESSOR_NUMBER],'CPU2': res[1][0],'CPU2_model': res[1][cs.CPU_PROCESSOR_NUMBER],'CPU3': res[2][0],'CPU3_model': res[2][cs.CPU_PROCESSOR_NUMBER],'Graph': my_plot_div})

def Step2(request):
    res = BI.get_cpu_recommendation()
 
    logger.warning("The value of CPU is %s", request.GET.get('CPU'))
    CPU = int(request.GET.get('CPU'))
    BI.set_gpu(res[int(CPU)])
    res = BI.get_gpu_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][cs.GPU_NAME],res[1][cs.GPU_NAME],res[2][cs.GPU_NAME]],
            y=[res[0][cs.GPU_PERFORMANCE_SCORE],res[1][cs.GPU_PERFORMANCE_SCORE], res[2][cs.GPU_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step2.html',{'GPU1': res[0][cs.GPU_NAME],'GPU1_model': res[0][cs.GPU_MANUFACTURER],'GPU2': res[1][cs.GPU_NAME],'GPU2_model': res[1][cs.GPU_MANUFACTURER],'GPU3': res[2][cs.GPU_NAME],'GPU3_model': res[2][cs.GPU_MANUFACTURER],'Graph': my_plot_div})

def Step3(request):
    res = BI.get_gpu_recommendation()
    logger.warning("The value of CPU is %s", request.GET.get('GPU'))
    GPU = request.GET.get('GPU')
    BI.set_gpu(res[int(GPU)])
    res = BI.get_cpu_recommendation()
    BI.set_cpu(res[int(CPU)])
    res = BI.get_memory_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][cs.MEMORY_NAME],res[1][cs.MEMORY_NAME],res[2][cs.MEMORY_NAME]],
            y=[res[0][cs.MEMORY_PERFORMANCE_SCORE],res[1][cs.MEMORY_PERFORMANCE_SCORE], res[2][cs.MEMORY_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step3.html',{'RAM1': res[0][cs.MEMORY_NAME],'RAM_model': res[0][cs.MEMORY_MANUFACTURER],'RAM2': res[1][cs.MEMORY_NAME],'RAM2_model': res[1][cs.MEMORY_MANUFACTURER],'RAM3': res[2][cs.MEMORY_NAME],'RAM3_model': res[2][cs.MEMORY_MANUFACTURER],'Graph': my_plot_div})

def Step4(request):
    res = BI.get_cpu_recommendation()
    logger.warning("The value of CPU is %s", res[int(CPU)])
    logger.warning("         ")
    BI.set_cpu(res[int(CPU)])

    res = BI.get_gpu_recommendation()

    logger.warning("The value of GPU is %s", res[int(GPU)])
    logger.warning("         ")
    BI.set_gpu(res[int(GPU)])

    res = BI.get_memory_recommendation()
    RAM = request.GET.get('RAM')
    logger.warning("The value of RAM is %s", res[int(RAM)])
    logger.warning("         ")
    BI.set_memory(res[int(RAM)])

    res = BI.get_storage_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][cs.STORAGE_NAME],res[1][cs.STORAGE_NAME],res[2][cs.STORAGE_NAME]],
            y=[res[0][cs.STORAGE_PERFORMANCE_SCORE],res[1][cs.STORAGE_PERFORMANCE_SCORE], res[2][cs.STORAGE_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step4.html',{'STORAGE1': res[0][cs.STORAGE_NAME],'STORAGE1_model': res[0][cs.STORAGE_MANUFACTURER],'STORAGE2': res[1][cs.STORAGE_NAME],'STORAGE2_model': res[1][cs.STORAGE_MANUFACTURER],'STORAGE3': res[2][cs.STORAGE_NAME],'STORAGE3_model': res[2][cs.STORAGE_MANUFACTURER],'Graph': my_plot_div})

def Step5(request):
    res = BI.get_cpu_recommendation()
    logger.warning("The value of CPU is %s", res[int(CPU)])
    logger.warning("         ")
    BI.set_cpu(res[int(CPU)])

    res = BI.get_gpu_recommendation()

    logger.warning("The value of GPU is %s", res[int(GPU)])
    logger.warning("         ")
    BI.set_gpu(res[int(GPU)])

    res = BI.get_memory_recommendation()
    RAM = request.GET.get('RAM')
    logger.warning("The value of RAM is %s", res[int(RAM)])
    logger.warning("         ")
    BI.set_memory(res[int(RAM)])

    res = BI.get_storage_recommendation()
    STORAGE = request.GET.get('STORAGE')
    BI.set_storage(res[int(STORAGE)])

    res = BI.get_motherboard_recommendation()

    my_plot_div = plot([go.Bar(
            x=[res[0][cs.MOTHERBOARD_NAME],res[1][cs.MOTHERBOARD_NAME],res[2][cs.MOTHERBOARD_NAME]],
            y=[res[0][cs.MOTHERBOARD_PERFORMANCE_SCORE],res[1][cs.MOTHERBOARD_PERFORMANCE_SCORE], res[2][cs.MOTHERBOARD_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step5.html',{'MB1': res[0][cs.MOTHERBOARD_NAME],'MB1_model': res[0][cs.MOTHERBOARD_MANUFACTURER],'MB2': res[1][cs.MOTHERBOARD_NAME],'MB2_model': res[1][cs.MOTHERBOARD_MANUFACTURER],'MB3': res[2][cs.MOTHERBOARD_NAME],'MB3_model': res[2][cs.MOTHERBOARD_MANUFACTURER],'Graph': my_plot_div})
