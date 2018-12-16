import sys
import os
import sklearn
import numpy as np
from sklearn import datasets, linear_model
import pdfkit
CAP_DIR = os.path.join(os.getcwd(),'cap')
import functools

sys.path.append(os.path.join(CAP_DIR,'PartsInfo')) #Path to BuildInfo directory
from django.shortcuts import render
from django.http import HttpResponse
from BuildInfo import BuildInfo
from CPUData import CPUData
from GPUData import GPUData
from MemoryData import MemoryData
from MotherboardData import MotherboardData
from StorageData import StorageData
from CSVinfo import *
import logging
import re
from plotly.offline import plot
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
path_wkthmltopdf = os.path.join(os.path.join(CAP_DIR,'static'),'wkhtmltopdf.exe')
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)




logger = logging.getLogger(__name__)
# Create your views here.
baseURL = CAP_DIR + '/datasets/'

BI = BuildInfo(baseURL+'cpu_clean.csv',baseURL+'gpu_clean.csv',baseURL+'memory_clean_new.csv',baseURL+'storage_clean.csv',baseURL+'motherboard_clean_new.csv')
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
    'Storage' : storage_name,'Storage_URL' : storage_url, 'Motherboard' : motherboard_name, 'Motherboard_URL' : motherboard_url,'Score' : score,'CPU_T' : CPU,
    'GPU_T' : GPU,'RAM_T' : RAM,'STORAGE_T' : STORAGE,'MB_T' : MB})

def Step7(request):
    url = "http://127.0.0.1:8000/Step6?CPU={}&GPU={}&RAM={}&STORAGE={}&MB={}".format(CPU,GPU,RAM,STORAGE,MB)

    pdf = pdfkit.from_url(url, False,configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="repo.pdf"'

    return response


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
    
def Step9(request):
    return render(request,'web/common.html')

def cpu_details(request):
    res = BI.get_all_cpus()
    Names = []
    score = []
    lith = []
    core = []
    thread = []
    base_freq = []
    catche = []
    tdp = []
    max_mem = []
    max_mem_bw = []
    graphics_base_freq = []
    graphics_max_freq = []
    # print(res[4][CPU_PERFORMANCE_SCORE])
    if(len(res)!=0):
        print(len(res))
        for i in range(len(res)-1):
            Names.append(res[i+1][CPU_PROCESSOR_NUMBER])
            score.append(CPUData.get_cpu_performance_score(res[i+1]))
            lith.append(CPUData.get_cpu_lithography(res[i+1]))
            core.append(int(res[i+1][CPU_NO_OF_CORES]))
            thread.append(int(res[i+1][CPU_NO_OF_THREADS]))
            base_freq.append(CPUData.get_cpu_base_frequency(res[i+1]))
            catche.append(CPUData.get_cpu_cache(res[i+1]))
            tdp.append(CPUData.get_cpu_tdp(res[i+1]))
            max_mem.append(CPUData.get_cpu_max_memory(res[i+1]))
            max_mem_bw.append(CPUData.get_cpu_max_memory_bandwidth(res[i+1]))
            graphics_base_freq.append(CPUData.get_cpu_graphics_base_freq(res[i+1]))
            graphics_max_freq.append(CPUData.get_cpu_graphics_max_mem(res[i+1]))

        graph = int(request.GET.get('graph'))  
        if(graph == 1):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=score,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 2):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=lith,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')

        if(graph == 3):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=core,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 4):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=thread,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
                print("call from graph 4")
        if(graph == 5):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=base_freq,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 6):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=catche,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 7):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=tdp,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 8):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=max_mem,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 9):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=max_mem_bw,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 10):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=graphics_base_freq,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 11):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=graphics_max_freq,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                ) ], output_type='div')
        
    else:
        print("Empty res Response")
    del res[0]
    print(graph)
    return render(request,'web/cpu_details.html' , {'Graph1' : my_plot_div ,'cpu_details' : res })

def motherboard_details(request):
    INTEL_ONLY = True  # set to False to include AMD motherboards
    csv_data = BI.get_all_motherboards()
    motherboard_details = []

    unique_dates_and_frequency = {}

    price_sum_per_unique_date = {}
    average_price_pre_unique_date = {}
    
    speed_sum_per_unique_date = {}
    average_speed_pre_unique_date = {}

    capacity_sum_per_unique_date = {}
    average_capacity_pre_unique_date = {}
    
    del csv_data[0]  # remove headers
    
    for row in csv_data:
        if INTEL_ONLY and not row[MOTHERBOARD_CPU_SOCKET].startswith('LGA'):
            continue
        
        date = row[MOTHERBOARD_LAUNCHED]
        
        motherboard_details.append([])

        # 0 : name
        motherboard_details[-1].append(row[MOTHERBOARD_NAME])
        
        # 1 : max memory supported
        capacity = int(MotherboardData.extract_num_data(row[MOTHERBOARD_MAXIMUM_SUPPORTED_MEMORY], 0, 'G'))
        motherboard_details[-1].append(str(capacity))

        # 2 : max memory speed
        all_speeds = row[MOTHERBOARD_MEMORY_TYPE][5:].split('/')
        speed = all_speeds[-1].strip()
        motherboard_details[-1].append(speed)

        # 3 : max ethernet speed
        speed = int(row[MOTHERBOARD_ONBOARD_ETHERNET][:-4].split('/')[-1].strip())
        if row[MOTHERBOARD_ONBOARD_ETHERNET].strip().endswith('Gbps'): speed *= 1000
        
        motherboard_details[-1].append(speed)

        # 4 : num of ethernet ports
        motherboard_details[-1].append(row[MOTHERBOARD_ONBOARD_ETHERNET].strip()[0])

        # 5 : price
        motherboard_details[-1].append(MotherboardData.get_motherboard_price(row))

        if date in unique_dates_and_frequency:
            price_sum_per_unique_date[date] += MotherboardData.get_motherboard_price(row)
            speed_sum_per_unique_date[date] += speed
            capacity_sum_per_unique_date[date] += capacity
            unique_dates_and_frequency[date] += 1
        else:
            price_sum_per_unique_date[date] = MotherboardData.get_motherboard_price(row)
            speed_sum_per_unique_date[date] = speed
            capacity_sum_per_unique_date[date] = capacity
            unique_dates_and_frequency[date] = 1

    
    for key, value in unique_dates_and_frequency.items():
        average_price_pre_unique_date[key] = price_sum_per_unique_date[key]/value
        average_speed_pre_unique_date[key] = speed_sum_per_unique_date[key]/value
        average_capacity_pre_unique_date[key] = capacity_sum_per_unique_date[key]/value

    dates = list(unique_dates_and_frequency.keys())
    dates.sort(key= functools.cmp_to_key(comp))

    list_of_prices = []
    list_of_speed = []
    list_of_capacity = []

    for date in dates:
        list_of_prices.append(average_price_pre_unique_date[date])
        list_of_speed.append(average_speed_pre_unique_date[date])
        list_of_capacity.append(average_capacity_pre_unique_date[date])

    return render(request, 'web/motherboard_details.html', {'motherboard_details':motherboard_details})

def comp(a,b):
    a_parts = a.split()
    b_parts = b.split()

    if int(a_parts[1]) > int(b_parts[1]):
        return 1
    elif int(a_parts[1]) == int(b_parts[1]):
        if int(a_parts[0][1]) > int(b_parts[0][1]):
            return 1
        elif  int(a_parts[0][1]) == int(b_parts[0][1]):
            return 0
        else:
            return -1
    else:
        return -1

def gpu_details(request):
    csv_data = BI.get_all_gpus()
    gpu_details = []

    del csv_data[0]  # remove headers
    
    Names = []
    Price = []
    Memeory_Size = []
    Memory_Speed = []
    Memory_Type = []
    Core_Speed = []
    Boost_Clock = []
    Max_Power = []

    for row in csv_data:
        
        gpu_details.append([])

        # 0 : Name
        Names.append(row[GPU_NAME])
        gpu_details[-1].append(row[GPU_NAME])
        
        # 1 : Memory Size
        mem_size = re.findall('\d+', row[GPU_MEMORY])[0]
        Memeory_Size.append(mem_size)
        gpu_details[-1].append(mem_size)

        # 2 : memory speed
        mem_speed = re.findall('\d+', row[GPU_MEMORY_SPEED])[0]
        Memory_Speed.append(mem_speed)
        gpu_details[-1].append(mem_speed)
        
        # 3 : memory type
        Memory_Type.append(row[GPU_MEMORY_TYPE])
        gpu_details[-1].append(row[GPU_MEMORY_TYPE])

        # 4 : Core SPEED
        core_speed = re.findall('\d+', row[GPU_CORE_SPEED])[0]
        Core_Speed.append(core_speed)
        gpu_details[-1].append(core_speed)

        # 5 : Boost clock
        x = re.findall('\d+', row[GPU_BOOST_CLOCK])
        boost_clock = 0
        if len(x) != 0:
            boost_clock = x[0] 
        Boost_Clock.append(boost_clock)
        gpu_details[-1].append(boost_clock)

        # 6 : max Power
        max_pow = re.findall('\d+', row[GPU_MAX_POWER])[0]
        Max_Power.append(max_pow)
        gpu_details[-1].append(max_pow)

        # 7 : price
        Price.append(GPUData.get_gpu_price(row))
        gpu_details[-1].append(GPUData.get_gpu_price(row))

    graph = int(request.GET.get('graph'))

    if(graph == 1):
        my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=Memeory_Size,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
    if(graph == 2):
        my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=Memory_Speed,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')

    if(graph == 3):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=Core_Speed,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
    if(graph == 4):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=Boost_Clock,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
                print("call from graph 4")
    if(graph == 5):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=Max_Power,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')
    if(graph == 6):
                my_plot_div = plot([go.Scatter(
                        x=Names,
                        y=Price,
                        mode = 'lines+markers',
                        name = 'lines+markers'
                )], output_type='div')

    return render(request, 'web/gpu_details.html', {'Graph1':my_plot_div,'gpu_details':gpu_details})




def memory_details(request):
    '''
		This function represents Memory details page
    '''
    csv_data = BI.get_all_memories()
    del csv_data[0]

    #print('+++++++++++',res,'++++++++++++\n\n\n')
    memory_details = []
    
    Name_mem = []
    Latency_mem = []
    Price_mem = []
    Size_mem = []
    Speed_mem = []
    Score_mem = []

    unique_dates_and_frequency = {}

    price_sum_per_unique_date = {}
    average_price_pre_unique_date = {}
    
    speed_sum_per_unique_date = {}
    average_speed_pre_unique_date = {}

    size_sum_per_unique_date = {}
    average_size_pre_unique_date = {}


    if(len(csv_data)!=0):
        """print(len(res))"""

        for row in csv_data:

            memory_details.append([])
            
            date = row[MEMORY_LAUNCHED]

            Name_mem.append(MemoryData.get_memory_name(row))
            memory_details[-1].append(MemoryData.get_memory_name(row))

            Latency_mem.append(MemoryData.get_memory_cas_latency(row))
            memory_details[-1].append(MemoryData.get_memory_cas_latency(row))

            Size_mem.append(MemoryData.get_memory_size(row))
            memory_details[-1].append(MemoryData.get_memory_size(row))

            Speed_mem.append(MemoryData.get_memory_speed(row))
            memory_details[-1].append(MemoryData.get_memory_speed(row))

            Price_mem.append(MemoryData.get_memory_price(row))
            memory_details[-1].append(MemoryData.get_memory_price(row))

            if date in unique_dates_and_frequency:
                price_sum_per_unique_date[date] += MemoryData.get_memory_price(row)
                speed_sum_per_unique_date[date] += MemoryData.get_memory_speed(row)
                size_sum_per_unique_date[date] += MemoryData.get_memory_size(row)
                unique_dates_and_frequency[date] += 1
            else:
                price_sum_per_unique_date[date] = MemoryData.get_memory_price(row)
                speed_sum_per_unique_date[date] = MemoryData.get_memory_speed(row)
                size_sum_per_unique_date[date] = MemoryData.get_memory_size(row)
                unique_dates_and_frequency[date] = 1    

            Score_mem.append(MemoryData.get_memory_performance_score(row))
        
        for key, value in unique_dates_and_frequency.items():
            average_price_pre_unique_date[key] = price_sum_per_unique_date[key]/value
            average_speed_pre_unique_date[key] = speed_sum_per_unique_date[key]/value
            average_size_pre_unique_date[key] = size_sum_per_unique_date[key]/value
        
        dates = list(unique_dates_and_frequency.keys())
        dates.sort(key= functools.cmp_to_key(comp))

        list_of_prices = []
        list_of_speed = []
        list_of_size = []

        for date in dates:
            list_of_prices.append(average_price_pre_unique_date[date])
            list_of_speed.append(average_speed_pre_unique_date[date])
            list_of_size.append(average_size_pre_unique_date[date])

            
        #print('__________________________________________',Latency_mem,'__________________________________________')
        #print('__________________________________________',Price_mem,'__________________________________________')
        #print('__________________________________________',Size_mem,'__________________________________________')
        #print('__________________________________________',ddr3_mem,'__________________________________________')
        #print('__________________________________________',score_mem,'__________________________________________')
        #print('__________________________________________',Name_mem,'__________________________________________')
        graph = int(request.GET.get('graph'))  
        if(graph == 1):
                my_plot_div = plot([go.Scatter(
                        x=Name_mem,
                        y=Latency_mem,
                        mode = 'markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 2):
                my_plot_div = plot([go.Scatter(
                        x=Name_mem,
                        y=Price_mem,
                        mode = 'markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 3):
                my_plot_div = plot([go.Scatter(
                        x=Name_mem,
                        y=Size_mem,
                        mode = 'markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 4):
                my_plot_div = plot([go.Scatter(
                        x=Name_mem,
                        y=Speed_mem,
                        mode = 'markers',
                        name = 'lines+markers'
                )], output_type='div')
        if(graph == 5):
                my_plot_div = plot([go.Scatter(
                        x=Name_mem,
                        y=score_mem,
                        mode = 'markers',
                        name = 'lines+markers'
                )], output_type='div')
    else:
        print("Empty res Response")
    #print(graph)
    return render(request,'web/memory_details.html' , {'Graph1' : my_plot_div ,'memory_details' : memory_details })