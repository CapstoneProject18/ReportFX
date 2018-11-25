from CPUData         import *
from CSVinfo         import *
from GPUData         import *
from MemoryData      import *
from MotherboardData import *
from StorageData     import *
import csv

# Ratio : CPU, GPU, RAM, Storage, Motherboard
USE_CSE_RATIO = {
                    'home'   : [0.3,0.1,0.2,0.3,0.1],
                    'gaming' : [0.2,0.3,0.3,0.1,0.1],
                    'office' : [0.3,0.1,0.3,0.2,0.1]
                }
BASE_COST_DELTA = 10     # max. difference between intended and actual cost
NUM_RECOMMENDATIONS = 5  # number of part recommendations

class BuildInfo:
    def __init__(self, cpu_filepath, gpu_filepath, memory_filepath, storage_filepath, \
                 motherboard_filepath):
        '''
        The constructor method to start a new system build.

        Arguments:
          cpu_filepath: path to the CSV containing CPU parts information.
          gpu_filepath: path to the CSV containing GPU parts information.
          memory_filepath: path to the CSV containing memory (RAM) parts information.
          storage_filepath: path to the CSV containing storage drive parts information.
          motherboard_filepath: path to the CSV containing motherboard parts information.
        
        Returns: Object of BuildInfo.
        '''
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
        '''
        Set the target cost and use case for the system.

        Arguments:
          target_cost: Intended system cost in USD. Must be a float value.
          use_case: Intended use case for the system. Must be one of the keys in USE_CASE_RATIO.
        
        Returns: None
        '''
        self.target_cost = target_cost
        self.use_case = use_case
        self.cost_ratio = USE_CSE_RATIO[use_case]
    
    def get_cpu_recommendation(self):
        '''
        Get CPU recommendations based on the base info.

        Arguments: None

        Returns: A list of NUM_RECOMMENDATIONS CPUs, in decreasing order of preference. Rows can
                 be indexed into using indices from CSVinfo.py.
        '''
        return self.get_recommendation(0, self.cpu_filepath, CPUData.get_cpu_price, \
                                       CPUData.get_cpu_performance_score, CPU_PERFORMANCE_SCORE)
    
    def set_cpu(self, cpu):
        '''
        Set CPU for the system.

        Arguments:
          cpu: List of CPU fields, exactly like the one returned by get_cpu_recommendation().
        
        Returns: None
        '''
        self.cpu = cpu
    
    def get_cpu(self):
        '''
        Returns the CPU set for the system.

        Arguments: None

        Returns: List of CPU fields, indexed using indices in CSVinfo.py.
        '''
        return self.cpu
    
    def get_gpu_recommendation(self):
        '''
        Get GPU recommendations based on the base info.

        Arguments: None

        Returns: A list of NUM_RECOMMENDATIONS GPUs, in decreasing order of preference. Rows can
                 be indexed into using indices from CSVinfo.py.
        '''
        return self.get_recommendation(1, self.gpu_filepath, GPUData.get_gpu_price, \
                                       GPUData.get_gpu_performance_score, GPU_PERFORMANCE_SCORE)

    def set_gpu(self, gpu):
        '''
        Set GPU for the system.

        Arguments:
          gpu: List of GPU fields, exactly like the one returned by get_gpu_recommendation().
        
        Returns: None
        '''
        self.gpu = gpu
    
    def get_gpu(self):
        '''
        Returns the GPU set for the system.

        Arguments: None

        Returns: List of GPU fields, indexed using indices in CSVinfo.py.
        '''
        return self.gpu
    
    def get_memory_recommendation(self):
        '''
        Get memory (RAM) recommendations based on the base info and CPU.

        Arguments: None

        Returns: A list of NUM_RECOMMENDATIONS RAM modules, in decreasing order of preference.
                 Rows can be indexed into using indices from CSVinfo.py.
        '''
        initial_recommendation = self.get_recommendation(2, self.memory_filepath, \
                                                         MemoryData.get_memory_price, \
                                                         MemoryData.get_memory_performance_score, \
                                                         MEMORY_PERFORMANCE_SCORE)
        
        is_ddr4_supported = True if 'DDR4' in self.cpu[CPU_MEMORY_TYPES] else False

        recommendation = []

        # filter row from the initial recommendation
        for row in initial_recommendation:
            # we don't want to keep DDR4 modules if the CPU doesn't support them
            if row[MEMORY_IS_DDR4] == 'TRUE' and not is_ddr4_supported:
                continue
            recommendation.append(row)
        
        return recommendation

    def set_memory(self, memory):
        '''
        Set RAM for the system.

        Arguments:
          memory: List of RAM fields, exactly like the one returned by get_memory_recommendation().
        
        Returns: None
        '''
        self.memory = memory
    
    def get_memory(self):
        '''
        Returns the RAM set for the system.

        Arguments: None

        Returns: List of RAM fields, indexed using indices in CSVinfo.py.
        '''
        return self.memory
    
    def get_storage_recommendation(self):
        '''
        Get storage drive recommendations based on the base info.

        Arguments: None

        Returns: A list of NUM_RECOMMENDATIONS storage drives, in decreasing order of preference.
                 Rows can be indexed into using indices from CSVinfo.py.
        '''
        return self.get_recommendation(3, self.storage_filepath, StorageData.get_storage_price, \
                                       StorageData.get_storage_performance_score, \
                                       STORAGE_PERFORMANCE_SCORE)

    def set_storage(self, storage):
        '''
        Set storage drive for the system.

        Arguments:
          storage: List of drive fields, exactly like the one returned by
                   get_storage_recommendation().
        
        Returns: None
        '''
        self.storage = storage
    
    def get_storage(self):
        '''
        Returns the storage drive set for the system.

        Arguments: None

        Returns: List of drive fields, indexed using indices in CSVinfo.py.
        '''
        return self.storage
    
    def get_motherboard_recommendation(self):
        '''
        Get motherboard recommendations based on the base info, CPU, GPU, and memory.

        Arguments: None

        Returns: A list of atleast 1 and atmost NUM_RECOMMENDATIONS motherboards, in decreasing
                 order of preference. Rows can be indexed into using indices from CSVinfo.py.
        '''
        cost_delta = BASE_COST_DELTA
        recommended_parts = []
        target_part_cost = self.target_cost * self.cost_ratio[4]

        # extract the required information from CPU, GPU and memory for compatibility
        cpu_socket = self.cpu[CPU_SOCKET]
        crossfire_required = self.gpu[GPU_MANUFACTURER] == 'AMD' and \
                             self.gpu[GPU_SLI_CROSSFIRE] == 'Yes'
        sli_required = self.gpu[GPU_MANUFACTURER] == 'Nvidia' and \
                       self.gpu[GPU_SLI_CROSSFIRE] == 'Yes'
        memory_size = MemoryData.extract_num_data(self.memory[MEMORY_SIZE], 0, 'G')
        memory_type = 'DDR4' if self.memory[MEMORY_IS_DDR4] == 'TRUE' else 'DDR3'

        # Get atleast one recommendation
        while (len(recommended_parts) < 1) and (cost_delta < target_part_cost):
            recommended_parts = []
            is_first_row = True

            with open(self.motherboard_filepath) as input_file:
                input_file_buffer = csv.reader(input_file, dialect='excel')
                for row in input_file_buffer:
                    # skip the first header row
                    if is_first_row:
                        is_first_row = False
                        continue
                    
                    # check if motherboard is within budget and meets specification
                    if (abs(MotherboardData.get_motherboard_price(row) - target_part_cost) <= cost_delta) and \
                       (cpu_socket in row[MOTHERBOARD_CPU_SOCKET]) and \
                       (not (crossfire_required and row[MOTHERBOARD_CROSSFIRE_SUPPORT] == 'No')) and \
                       (not (sli_required and row[MOTHERBOARD_SLI_SUPPORT] == 'No')) and \
                       (memory_size <= MotherboardData.extract_num_data(row[MOTHERBOARD_MAXIMUM_SUPPORTED_MEMORY], 0, 'G')) and \
                       (memory_type in row[MOTHERBOARD_MEMORY_TYPE]):
                        recommended_parts.append(row)
            
            # increase cost delta for next iteration
            cost_delta *= 2
                
        # Calculate performance scores and sort
        for row in recommended_parts:
            row.append(MotherboardData.get_motherboard_performance_score(row))
        recommended_parts.sort(key=lambda x:x[MOTHERBOARD_PERFORMANCE_SCORE], reverse=True)

        return recommended_parts
    
    def set_motherboard(self, motherboard):
        '''
        Set motherboard for the system.

        Arguments:
          motherboard: List of motherboard fields, exactly like the one returned by
                       get_motherboard_recommendation().
        
        Returns: None
        '''
        self.motherboard = motherboard
    
    def get_motherboard(self):
        '''
        Returns the motherboard set for the system.

        Arguments: None

        Returns: List of motherboard fields, indexed using indices in CSVinfo.py.
        '''
        return self.motherboard
    
    def get_recommendation(self, ratio_index, filepath, price_function, performance_function, \
                           performance_score_index):
        '''
        The base recommendation function. Returns NUM_RECOMMENDATIONS recommendations based on the
        target price, trying to maximize performance score and minimize cost delta.

        Arguments:
          ratio_index: Ratio of the target_price set aside for this component.
          filepath: Path to CSV of the part.
          price_function: Pointer to the function that can return the price of each part when
                          provided with a row from the CSV.
          performance_function: Pointer to the function that can return the performance score of
                                each part when provided with a row from the CSV.
          performance_score_index: Index in which the calculated performance will get stored.
        
        Returns: NUM_RECOMMENDATIONS recommendations in decreasing order of preference.
        '''
        cost_delta = BASE_COST_DELTA
        recommended_parts = []
        target_part_cost = self.target_cost * self.cost_ratio[ratio_index]
        is_first_row = True

        # Get the minimum recommendations
        while len(recommended_parts) < NUM_RECOMMENDATIONS:
            recommended_parts = []
            is_first_row = True

            with open(filepath) as input_file:
                input_file_buffer = csv.reader(input_file, dialect='excel')
                for row in input_file_buffer:
                    # skip the first header row
                    if is_first_row:
                        is_first_row = False
                        continue

                    # check if the part is within budget
                    if abs(price_function(row) - target_part_cost) <= cost_delta:
                        recommended_parts.append(row)
            
            # increase cost delta for next iteration
            cost_delta *= 2
                
        # Calculate performance scores and sort
        for row in recommended_parts:
            row.append(performance_function(row))
        recommended_parts.sort(key=lambda x:x[performance_score_index], reverse=True)
        
        return recommended_parts
