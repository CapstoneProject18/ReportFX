from CPUData import *
from CSVinfo import *
import csv
from GPUData import *
from MemoryData import *

# Ratio : CPU, GPU, RAM, Storage, Motherboard
USE_CSE_RATIO = {
                    'home'   : [0.3,0.1,0.2,0.3,0.1],
                    'gaming' : [0.2,0.3,0.2,0.2,0.1],
                    'office' : [0.2,0.2,0.2,0.2,0.2]
                }

BASE_COST_DELTA = 10

class BuildInfo:
    def __init__(self, cpu_filepath, gpu_filepath, memory_filepath, storage_filepath, \
                 motherboard_filepath):
        self.cpu_filepath = cpu_filepath
        self.gpu_filepath = gpu_filepath
        self.memory_filepath = memory_filepath
        self.storage_filepath = storage_filepath
        self.motherboard_filepath = motherboard_filepath

        self.target_cost = 0
        self.use_case = 0
        self.cost_ratio = []

        self.cpu = []
        self.gpu = []
        self.memory = []
        self.storage = []
        self.motherboard = []
    
    def set_base_info(self, target_cost, use_case):
        self.target_cost = target_cost
        self.use_case = use_case
        self.cost_ratio = USE_CSE_RATIO[use_case]
    
    def get_cpu_recommendation(self):
        return self.get_recommendation(0, self.cpu_filepath, CPUData.get_cpu_price, \
                                       CPUData.get_cpu_performance_score, CPU_PERFORMANCE_SCORE)
    
    def set_cpu(self, cpu):
        self.cpu = cpu
    
    def get_gpu_recommendation(self):
        return self.get_recommendation(1, self.gpu_filepath, GPUData.get_gpu_price, \
                                       GPUData.get_gpu_performance_score, GPU_PERFORMANCE_SCORE)

    def set_gpu(self, gpu):
        self.gpu = gpu
    
    def get_memory_recommendation(self):
        initial_recommendation = self.get_recommendation(1, self.memory_filepath, \
                                                         MemoryData.get_memory_price, \
                                                         MemoryData.get_memory_performance_score, \
                                                         MEMORY_PERFORMANCE_SCORE)
        
        is_ddr4_supported = True if 'DDR4' in self.cpu[CPU_MEMORY_TYPES] else False

        recommendation = []

        for row in initial_recommendation:
            if row[MEMORY_IS_DDR4] == 'TRUE' and not is_ddr4_supported:
                continue
            recommendation.append(row)
        
        return recommendation

    def set_memory(self, memory):
        self.memory = memory
    
    def set_storage(self, storage):
        self.storage = storage
    
    def set_motherboard(self, motherboard):
        self.motherboard = motherboard
    
    def get_recommendation(self, ratio_index, filepath, price_function, performance_function, \
                           performance_score_index):
        cost_delta = BASE_COST_DELTA
        recommended_parts = []
        target_part_cost = self.target_cost * self.cost_ratio[ratio_index]
        is_first_row = True

        # Get atleast three recommendations
        while len(recommended_parts) < 3:
            recommended_parts = []
            is_first_row = True

            with open(filepath) as input_file:
                input_file_buffer = csv.reader(input_file, dialect='excel')
                for row in input_file_buffer:
                    # skip the first header row
                    if is_first_row:
                        is_first_row = False
                        continue

                    # check if GPU is within budget
                    if abs(price_function(row) - target_part_cost) <= cost_delta:
                        recommended_parts.append(row)
            
            # increase cost delta for next iteration
            cost_delta *= 2
                
        # Calculate performance scores and sort
        for row in recommended_parts:
            row.append(performance_function(row))
        recommended_parts.sort(key=lambda x:x[performance_score_index], reverse=True)
        
        return recommended_parts
