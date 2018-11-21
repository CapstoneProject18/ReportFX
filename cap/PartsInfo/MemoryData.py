from CSVinfo import *

class MemoryData:    
    def get_memory_price(row):
        return MemoryData.extract_num_data(row[MEMORY_PRICES], 1, ',')
    
    def get_memory_performance_score(row):
        return MemoryData.get_memory_cas_latency(row) + \
        (10 if MemoryData.is_memory_ecc_supported(row) else 0) + \
        (10 if MemoryData.is_memory_heat_spreader_supported(row) else 0) + \
        abs(MemoryData.get_memory_size(row) * 5) + \
        (abs(MemoryData.get_memory_ddr4_speed(row) / 100) if MemoryData.is_memory_ddr4(row) \
         else abs(MemoryData.get_memory_ddr3_speed(row) / 100))

    def extract_num_data(col, start, str):
        if str not in col:
            return 0
        return float(col[start:col.find(str)])
    
    def get_memory_cas_latency(row):
        return float(row[MEMORY_CAS_LATENCY])
    
    def is_memory_ecc_supported(row):
        return True if row[MEMORY_ECC] == 'Yes' else False
    
    def is_memory_heat_spreader_supported(row):
        return True if row[MEMORY_HEAT_SPREADER] == 'Yes' else False
    
    def get_memory_size(row):
        return MemoryData.extract_num_data(row[MEMORY_SIZE], 0, 'G')
    
    def is_memory_ddr4(row):
        return True if row[MEMORY_IS_DDR4] == 'FALSE' else False
    
    def get_memory_ddr3_speed(row):
        return float(row[MEMORY_DDR3_SPEED])
    
    def get_memory_ddr4_speed(row):
        return float(row[MEMORY_DDR4_SPEED])
