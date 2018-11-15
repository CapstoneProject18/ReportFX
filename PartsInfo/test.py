#!/usr/bin/python3
from BuildInfo import *

bi = BuildInfo('Datasets/Intel_CPUs_clean.csv', 'Datasets/All_GPUs_Clean.csv', 'Datasets/memory_clean.csv', 'Datasets/storage_clean.csv', 'Datasets/motherboard_clean.csv')
bi.set_base_info(1000, 'home')

cpu_recommendation = bi.get_cpu_recommendation()
for row in cpu_recommendation:
    print(row[CPU_PROCESSOR_NUMBER] + ', ' + row[CPU_RECOMMENDED_PRICE])
bi.set_cpu(cpu_recommendation[0])

print()
gpu_recommendation = bi.get_gpu_recommendation()
for row in gpu_recommendation:
    print(row[GPU_NAME] + ', ' + row[GPU_RELEASE_PRICE])
bi.set_gpu(gpu_recommendation[0])

print()
memory_recommendation = bi.get_memory_recommendation()
for row in memory_recommendation:
    print(row[MEMORY_NAME] + ', ' + row[MEMORY_PRICES])
bi.set_memory(memory_recommendation[0])

print()
storage_recommendation = bi.get_storage_recommendation()
for row in storage_recommendation:
    print(row[STORAGE_NAME] + ', ' + row[STORAGE_PRICES])
bi.set_storage(storage_recommendation[0])

print()
motherboard_recommendation = bi.get_motherboard_recommendation()
for row in motherboard_recommendation:
    print(row[MOTHERBOARD_NAME] + ', ' + row[MOTHERBOARD_PRICES])
bi.set_motherboard(motherboard_recommendation[0])
