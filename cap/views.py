import sys
import os
import pdfkit
CAP_DIR = os.path.join(os.getcwd(),'cap')

sys.path.append(os.path.join(CAP_DIR,'PartsInfo')) #Path to BuildInfo directory
from django.shortcuts import render
from BuildInfo import BuildInfo
import CSVinfo as cs
from CSVinfo import *
import logging
from plotly.offline import plot
import plotly.graph_objs as go

path_wkthmltopdf = os.path.join(os.path.join(CAP_DIR,'static'),'wkhtmltopdf.exe')
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)




logger = logging.getLogger(__name__)
# Create your views here.
baseURL = CAP_DIR + '/datasets/'

BI = BuildInfo(baseURL+'cpu_clean.csv',baseURL+'gpu_clean.csv',baseURL+'memory_clean.csv',baseURL+'storage_clean.csv',baseURL+'motherboard_clean.csv')
CPU = 0
GPU= 0
RAM = 0
STORAGE = 0
MB = 0
def index(request):
    return render(request,'web/welcomePage.html')

def Step1(request):
    BI.set_base_info(int(request.GET.get('price')),request.GET.get('type'))
    res = BI.get_cpu_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][cs.CPU_PROCESSOR_NUMBER],res[1][cs.CPU_PROCESSOR_NUMBER],res[2][cs.CPU_PROCESSOR_NUMBER]],
            y=[res[0][cs.CPU_PERFORMANCE_SCORE],res[1][cs.CPU_PERFORMANCE_SCORE], res[2][cs.CPU_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step1.html',{'CPU1': res[0][0],'CPU1_model': res[0][cs.CPU_PROCESSOR_NUMBER],'CPU2': res[1][0],'CPU2_model': res[1][cs.CPU_PROCESSOR_NUMBER],'CPU3': res[2][0],'CPU3_model': res[2][cs.CPU_PROCESSOR_NUMBER],'Graph': my_plot_div})

def Step2(request):
    res = BI.get_cpu_recommendation()
 
    logger.warning("The value of CPU is %s", request.GET.get('CPU'))
    CPU = int(request.GET.get('CPU'))
    BI.set_cpu(res[int(CPU)])
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

    res = BI.get_memory_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][cs.MEMORY_NAME],res[1][cs.MEMORY_NAME],res[2][cs.MEMORY_NAME]],
            y=[res[0][cs.MEMORY_PERFORMANCE_SCORE],res[1][cs.MEMORY_PERFORMANCE_SCORE], res[2][cs.MEMORY_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step3.html',{'RAM1': res[0][cs.MEMORY_NAME],'RAM_model': res[0][cs.MEMORY_MANUFACTURER],'RAM2': res[1][cs.MEMORY_NAME],'RAM2_model': res[1][cs.MEMORY_MANUFACTURER],'RAM3': res[2][cs.MEMORY_NAME],'RAM3_model': res[2][cs.MEMORY_MANUFACTURER],'Graph': my_plot_div})

def Step4(request):
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
    res = BI.get_storage_recommendation()
    STORAGE = request.GET.get('STORAGE')
    BI.set_storage(res[int(STORAGE)])

    res = BI.get_motherboard_recommendation()

    my_plot_div = plot([go.Bar(
            x=[res[0][cs.MOTHERBOARD_NAME],res[1][cs.MOTHERBOARD_NAME],res[2][cs.MOTHERBOARD_NAME]],
            y=[res[0][cs.MOTHERBOARD_PERFORMANCE_SCORE],res[1][cs.MOTHERBOARD_PERFORMANCE_SCORE], res[2][cs.MOTHERBOARD_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step5.html',{'MB1': res[0][cs.MOTHERBOARD_NAME],'MB1_model': res[0][cs.MOTHERBOARD_MANUFACTURER],'MB2': res[1][cs.MOTHERBOARD_NAME],'MB2_model': res[1][cs.MOTHERBOARD_MANUFACTURER],'MB3': res[2][cs.MOTHERBOARD_NAME],'MB3_model': res[2][cs.MOTHERBOARD_MANUFACTURER],'Graph': my_plot_div})



def Step6(request):
    res = BI.get_motherboard_recommendation()
    MB = request.GET.get('MB')

    cpu = BI.get_cpu()
    gpu = BI.get_gpu()
    memory = BI.get_memory()
    storage = BI.get_storage()
    motherboard = res[int(MB)]

    cpu_name = cpu[CPU_PROCESSOR_FAMILY] + " " + cpu[CPU_PROCESSOR_NUMBER]
    gpu_name = gpu[GPU_MANUFACTURER] + " " + gpu[GPU_NAME]
    memory_name = memory[MEMORY_NAME]
    storage_name =  storage[STORAGE_NAME]
    motherboard_name =  motherboard[MOTHERBOARD_NAME]

    cpu_url,gpu_url,memory_url,storage_url,motherboard_url = createAmazonURL(cpu_name,gpu_name,memory_name,storage_name,motherboard_name)

    score = int(cpu[CPU_PERFORMANCE_SCORE] + gpu[GPU_PERFORMANCE_SCORE] + memory[MEMORY_PERFORMANCE_SCORE] + storage[STORAGE_PERFORMANCE_SCORE] + motherboard[MOTHERBOARD_PERFORMANCE_SCORE])
        
    return render(request,'web/Step6.html',{'CPU' : cpu_name,'CPU_URL' : cpu_url,'GPU' : gpu_name,'GPU_URL': gpu_url,'Memory' : memory_name,'Memory_URL': memory_url,
    'Storage' : storage_name,'Storage_URL' : storage_url, 'Motherboard' : motherboard_name, 'Motherboard_URL' : motherboard_url,'Score' : score})

def Step7(request):
    url = "http://127.0.0.1:8000/Step6?CPU={}&GPU={}&RAM={}&STORAGE={}&MB={}".format(CPU,GPU,RAM,STORAGE,MB)

    pdfkit.from_url(url, "out.pdf", configuration=config)
    return render(request,'web/Step7.html')


# def pdfReport(request):
#     return render(request,'web/pdfReport.html')

def createAmazonURL(cpu_name,gpu_name,memory_name,storage_name,motherboard_name):
    base_url = "https://www.amazon.com/s?url=search-alias%3Daps&field-keywords="
    cpu_url = base_url + cpu_name.replace(" ","+")
    gpu_url = base_url + gpu_name.replace(" ","+")
    memory_url = base_url + memory_name.replace(" ","+")
    storage_url = base_url + storage_name.replace(" ","+")
    motherboard_url = base_url + motherboard_name.replace(" ","+")
    return cpu_url,gpu_url,memory_url,storage_url,motherboard_url


cart_content = dict()
def Step8(request):
    cpu = BI.get_cpu()
    gpu = BI.get_gpu()
    memory = BI.get_memory()
    storage = BI.get_storage()
    if(gpu!=None):
        cart_content['GPU'] = gpu[GPU_NAME]
    if(cpu!=None):
        cart_content['CPU'] = cpu[CPU_PROCESSOR_FAMILY]
    if(memory!=None):
        cart_content['RAM'] = memory[MEMORY_NAME]
    if(storage!=None):
        cart_content['HDD'] = storage[STORAGE_NAME]



 #   if(SSD!=None):
 #       cart_content['SSD'] = SSD
    print(cart_content)
    return render(request,'web/cart.html',{'cart_content':cart_content})
    