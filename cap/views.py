import sys
import os
import pdfkit
CAP_DIR = os.path.join(os.getcwd(),'cap')

sys.path.append(os.path.join(CAP_DIR,'PartsInfo')) #Path to BuildInfo directory
from django.shortcuts import render
from BuildInfo import BuildInfo
from CPUData import CPUData
from GPUData import GPUData
from MemoryData import MemoryData
from MotherboardData import MotherboardData
from StorageData import StorageData
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
CPU = -1
GPU= -1
RAM = -1
STORAGE = -1
MB = -1
def index(request):
    return render(request,'web/welcomePage.html')

def Step1(request):
    global MB,CPU,GPU,STORAGE,RAM
    BI.set_base_info(int(request.GET.get('price')),request.GET.get('type'))
    res = BI.get_cpu_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][CPU_PROCESSOR_NUMBER],res[1][CPU_PROCESSOR_NUMBER],res[2][CPU_PROCESSOR_NUMBER]],
            y=[res[0][CPU_PERFORMANCE_SCORE],res[1][CPU_PERFORMANCE_SCORE], res[2][CPU_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step1.html',{'CPU1': res[0][0],'CPU1_model': res[0][CPU_PROCESSOR_NUMBER],'CPU1_price': CPUData.get_cpu_price(res[0]), \
                                            'CPU2': res[1][0],'CPU2_model': res[1][CPU_PROCESSOR_NUMBER],'CPU2_price': CPUData.get_cpu_price(res[1]), \
                                            'CPU3': res[2][0],'CPU3_model': res[2][CPU_PROCESSOR_NUMBER],'CPU3_price': CPUData.get_cpu_price(res[2]), \
                                            'Graph': my_plot_div})

def Step2(request):
    global MB,CPU,GPU,STORAGE,RAM
    res = BI.get_cpu_recommendation()
 
    logger.warning("The value of CPU is %s", request.GET.get('CPU'))
    CPU = int(request.GET.get('CPU'))
    BI.set_cpu(res[int(CPU)])
    res = BI.get_gpu_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][GPU_NAME],res[1][GPU_NAME],res[2][GPU_NAME]],
            y=[res[0][GPU_PERFORMANCE_SCORE],res[1][GPU_PERFORMANCE_SCORE], res[2][GPU_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step2.html',{'GPU1': res[0][GPU_NAME],'GPU1_model': res[0][GPU_MANUFACTURER],'GPU1_price': GPUData.get_gpu_price(res[0]), \
                                            'GPU2': res[1][GPU_NAME],'GPU2_model': res[1][GPU_MANUFACTURER],'GPU2_price': GPUData.get_gpu_price(res[1]), \
                                            'GPU3': res[2][GPU_NAME],'GPU3_model': res[2][GPU_MANUFACTURER],'GPU3_price': GPUData.get_gpu_price(res[2]), \
                                            'Graph': my_plot_div})

def Step3(request):
    global MB,CPU,GPU,STORAGE,RAM
    res = BI.get_gpu_recommendation()
    logger.warning("The value of CPU is %s", request.GET.get('GPU'))
    GPU = request.GET.get('GPU')
    BI.set_gpu(res[int(GPU)])

    res = BI.get_memory_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][MEMORY_NAME],res[1][MEMORY_NAME],res[2][MEMORY_NAME]],
            y=[res[0][MEMORY_PERFORMANCE_SCORE],res[1][MEMORY_PERFORMANCE_SCORE], res[2][MEMORY_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step3.html',{'RAM1': res[0][MEMORY_NAME],'RAM1_model': res[0][MEMORY_MANUFACTURER],'RAM1_price': MemoryData.get_memory_price(res[0]), \
                                            'RAM2': res[1][MEMORY_NAME],'RAM2_model': res[1][MEMORY_MANUFACTURER],'RAM2_price': MemoryData.get_memory_price(res[1]),\
                                            'RAM3': res[2][MEMORY_NAME],'RAM3_model': res[2][MEMORY_MANUFACTURER],'RAM3_price': MemoryData.get_memory_price(res[2]), \
                                            'Graph': my_plot_div})

def Step4(request):
    global MB,CPU,GPU,STORAGE,RAM
    res = BI.get_memory_recommendation()
    RAM = request.GET.get('RAM')
    logger.warning("The value of RAM is %s", res[int(RAM)])
    logger.warning("         ")
    BI.set_memory(res[int(RAM)])

    res = BI.get_storage_recommendation()
    my_plot_div = plot([go.Bar(
            x=[res[0][STORAGE_NAME],res[1][STORAGE_NAME],res[2][STORAGE_NAME]],
            y=[res[0][STORAGE_PERFORMANCE_SCORE],res[1][STORAGE_PERFORMANCE_SCORE], res[2][STORAGE_PERFORMANCE_SCORE]]
    )], output_type='div')
    return render(request,'web/Step4.html',{'STORAGE1': res[0][STORAGE_NAME],'STORAGE1_model': res[0][STORAGE_MANUFACTURER],'STORAGE1_price': StorageData.get_storage_price(res[0]), \
                                            'STORAGE2': res[1][STORAGE_NAME],'STORAGE2_model': res[1][STORAGE_MANUFACTURER],'STORAGE2_price': StorageData.get_storage_price(res[1]), \
                                            'STORAGE3': res[2][STORAGE_NAME],'STORAGE3_model': res[2][STORAGE_MANUFACTURER],'STORAGE3_price': StorageData.get_storage_price(res[2]), \
                                            'Graph': my_plot_div})

def Step5(request):
    global MB,CPU,GPU,STORAGE,RAM
    res = BI.get_storage_recommendation()
    STORAGE = request.GET.get('STORAGE')
    BI.set_storage(res[int(STORAGE)])

    res = BI.get_motherboard_recommendation()

    string_name = ""
    string_score = ""
    for r in range(len(res)):
        string_name += res[r][MOTHERBOARD_NAME]
        string_score += str(res[r][MOTHERBOARD_PERFORMANCE_SCORE])
        if(r == (len(res)-1)):
            pass
        else:
            string_name += ","
            string_score += ","
    logger.warning("******   "+string_name+"    "+string_score)
    
    MB_list = []
    MB_model = []
    MB_score = []
    MB_price = []
    for r in range(len(res)):
        MB_list.append(res[r][MOTHERBOARD_NAME])
        MB_model.append(res[r][MOTHERBOARD_MANUFACTURER])
        MB_score.append(res[r][MOTHERBOARD_PERFORMANCE_SCORE])
        MB_price.append(MotherboardData.get_motherboard_price(res[r]))
    
    my_plot_div = plot([go.Bar(
            x=MB_list,
            y=MB_score
    )], output_type='div')
    my_list = zip(MB_list,MB_model,MB_price)
    return render(request,'web/Step5.html',{'Graph': my_plot_div ,'MB_list' : my_list})



def Step6(request):
    global MB,CPU,GPU,STORAGE,RAM
    res = BI.get_motherboard_recommendation()
    MB = request.GET.get('MB')
    BI.set_motherboard(res[int(MB)])
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



def Step8(request):
    
    cart_content = list()
    cart_price = list()
    
    cpu = BI.get_cpu()
    gpu = BI.get_gpu()
    memory = BI.get_memory()
    storage = BI.get_storage()
    mb = BI.get_motherboard()

    if(GPU!=-1):
        if(gpu[GPU_NAME] not in cart_content):
            cart_content.append(gpu[GPU_NAME])
            cart_price.append(GPUData.get_gpu_price(gpu))
    if(CPU!=-1):
        if((cpu[CPU_PROCESSOR_FAMILY] + ' ' + cpu[CPU_PROCESSOR_NUMBER]) not in cart_content):
            cart_content.append(cpu[CPU_PROCESSOR_FAMILY] + ' ' + cpu[CPU_PROCESSOR_NUMBER])
            cart_price.append(CPUData.get_cpu_price(cpu))
    if(RAM!=-1):
        if(memory[MEMORY_NAME] not in cart_content):
            cart_content.append(memory[MEMORY_NAME])
            cart_price.append(MemoryData.get_memory_price(memory))
    if(STORAGE!=-1):
        if(storage[STORAGE_NAME] not in cart_content):
            cart_content.append(storage[STORAGE_NAME])
            cart_price.append(StorageData.get_storage_price(storage))
    if(MB!=-1):
        if(mb[MOTHERBOARD_NAME] not in cart_content):
            cart_content.append(mb[MOTHERBOARD_NAME])
            cart_price.append(MotherboardData.get_motherboard_price(mb))
    
    list_cart = zip(cart_content,cart_price)
    #print(cart_content)
    return render(request,'web/cart.html',{'cart_content':list_cart})
    