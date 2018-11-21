from CSVinfo import *

class CPUData:    
    def get_cpu_price(row):
        price = row[CPU_RECOMMENDED_PRICE]
        return CPUData.extract_num_data(price, 1, '-')
    
    def get_cpu_performance_score(row):
        return abs(100 / CPUData.get_cpu_lithography(row)) + \
        (int(row[CPU_NO_OF_CORES]) * 5) + \
        (int(row[CPU_NO_OF_THREADS]) * 5) + \
        abs(CPUData.get_cpu_base_frequency(row) * 2) + \
        abs(CPUData.get_cpu_turbo_frequency(row)) + \
        abs(CPUData.get_cpu_cache(row) * 3) + \
        abs(1000 / CPUData.get_cpu_tdp(row)) + \
        CPUData.get_cpu_max_memory(row) + \
        (3 * CPUData.get_cpu_mem_channels(row)) + \
        (2 * CPUData.get_cpu_max_memory_bandwidth(row)) + \
        (10 if CPUData.cpu_is_ecc_supported(row) else 0) + \
        (CPUData.get_cpu_graphics_base_freq(row) / 10) + \
        (10 * CPUData.get_cpu_graphics_max_freq(row)) + \
        CPUData.get_cpu_graphics_max_mem(row) + \
        (CPUData.get_cpu_T(row) / 10) + \
        (20 if CPUData.cpu_is_ht_supported(row) else 0) + \
        (10 if CPUData.cpu_is_secure_key_supported(row) else 0)

    def extract_num_data(col, start, str):
        if str not in col:
            return 0
        return float(col[start:col.find(str)])
    
    def get_cpu_lithography(row):
        lithography = row[CPU_LITHOGRAPHY]
        return CPUData.extract_num_data(lithography, 0, 'n')

    def get_cpu_base_frequency(row):
        frequency = row[CPU_BASE_FREQUENCY]
        return CPUData.extract_num_data(frequency, 0, 'G')
    
    def get_cpu_turbo_frequency(row):
        frequency = row[CPU_MAX_TURBO_FREQUENCY]
        return CPUData.extract_num_data(frequency, 0, 'G')
    
    def get_cpu_cache(row):
        cache = row[CPU_CACHE]
        return CPUData.extract_num_data(cache, 0, 'M')
    
    def get_cpu_tdp(row):
        tdp = row[CPU_TDP]
        return CPUData.extract_num_data(tdp, 0, 'W')
    
    def get_cpu_max_memory(row):
        mem = row[CPU_MAX_MEMORY]
        return CPUData.extract_num_data(mem, 0, 'G')
    
    def get_cpu_mem_channels(row):
        return int(row[CPU_NO_OF_MEMORY_CHANNELS])
    
    def get_cpu_max_memory_bandwidth(row):
        bw = row[CPU_MAX_MEMORY_BANDWIDTH]
        return CPUData.extract_num_data(bw, 0, 'G')
    
    def cpu_is_ecc_supported(row):
        return True if row[CPU_ECC_MEMORY_SUPPORT] == 'Yes' else False
    
    def get_cpu_graphics_base_freq(row):
        frequency = row[CPU_GRAPHICS_BASE_FREQUENCY]
        return CPUData.extract_num_data(frequency, 0, 'M')
    
    def get_cpu_graphics_max_freq(row):
        frequency = row[CPU_GRAPHICS_BASE_FREQUENCY]
        freq = CPUData.extract_num_data(frequency, 0, 'M')

        if freq != 0:
            return freq / 1000
        else:
            return CPUData.extract_num_data(frequency, 0, 'G')

    def get_cpu_graphics_max_mem(row):
        mem = row[CPU_GRAPHICS_MAX_MEMORY]
        return CPUData.extract_num_data(mem, 0, 'G')
    
    def get_cpu_T(row):
        temp = row[CPU_T]
        return CPUData.extract_num_data(temp, 0, 'Â')
    
    def cpu_is_ht_supported(row):
        return True if row[CPU_HT] == 'Yes' else False
    
    def cpu_is_secure_key_supported(row):
        return True if row[CPU_SECURE_KEY] == 'Yes' else False
