from CSVinfo import *

class GPUData:
    def get_gpu_price(row):
        return float(row[GPU_RELEASE_PRICE][1:])
    
    def get_gpu_performance_score(row):
        return abs(GPUData.get_gpu_boost_clock(row) / 100) + \
        abs(GPUData.get_gpu_core_speed(row) / 10) + \
        abs(GPUData.get_gpu_dvi_connection(row) * 5) + \
        abs(GPUData.get_gpu_hdmi_connection(row) * 5) + \
        abs(GPUData.get_gpu_l2_cache(row) / 10) + \
        abs(1000 / GPUData.get_gpu_max_power(row)) + \
        abs(GPUData.get_gpu_memory(row) / 100) + \
        abs(GPUData.get_gpu_memory_bandwidth(row) / 10) + \
        abs(GPUData.get_gpu_memory_speed(row) / 100) + \
        GPUData.get_gpu_memory_type_score(row) + \
        abs(GPUData.get_gpu_pixel_rate(row) / 10) + \
        abs(100 / GPUData.get_gpu_process(row)) + \
        (10 if GPUData.is_gpu_sli_crossfire_supported(row) else 0) + \
        abs(GPUData.get_gpu_texture_rate(row) / 10) + \
        abs(GPUData.get_gpu_vga_connection(row) * 5)

    def extract_num_data(col, start, str):
        if str not in col:
            return 0
        
        value = 0
        try:
            value = float(col[start:col.find(str)])
        except ValueError:
            return 0
        
        return value
    
    def get_gpu_boost_clock(row):
        frequency = row[GPU_BOOST_CLOCK]
        return GPUData.extract_num_data(frequency, 0, 'M')
    
    def get_gpu_core_speed(row):
        frequency = row[GPU_CORE_SPEED]
        return GPUData.extract_num_data(frequency, 0, 'M')
    
    def get_gpu_dvi_connection(row):
        value = 0
        try:
            value = int(row[GPU_DVI_CONNECTION])
        except ValueError:
            return 0
        
        return value
    
    def get_gpu_hdmi_connection(row):
        return int(row[GPU_HDMI_CONNECTION])
    
    def get_gpu_l2_cache(row):
        memory = row[GPU_L2_CACHE]
        return GPUData.extract_num_data(memory, 0, 'K')
    
    def get_gpu_max_power(row):
        power = row[GPU_MAX_POWER]
        return GPUData.extract_num_data(power, 0, 'W')
    
    def get_gpu_memory(row):
        memory = row[GPU_MEMORY]
        return GPUData.extract_num_data(memory, 0, 'M')
    
    def get_gpu_memory_bandwidth(row):
        bw = row[GPU_MEMORY_BANDWIDTH]
        return GPUData.extract_num_data(bw, 0, 'G')
    
    def get_gpu_memory_speed(row):
        frequency = row[GPU_MEMORY_SPEED]
        return GPUData.extract_num_data(frequency, 0, 'M')
    
    def get_gpu_memory_type_score(row):
        memory_type = row[GPU_MEMORY_TYPE]
        
        if memory_type in ['GDDR5', 'HBM-1']:
            return 20
        elif memory_type in ['GDDR5X', 'HBM-2']:
            return 40
        
        return 10
    
    def get_gpu_pixel_rate(row):
        rate = row[GPU_PIXEL_RATE]
        return GPUData.extract_num_data(rate, 0, 'G')
    
    def get_gpu_process(row):
        process = row[GPU_PROCESS]
        return GPUData.extract_num_data(process, 0, 'n')

    def is_gpu_sli_crossfire_supported(row):
        return True if row[GPU_SLI_CROSSFIRE] == 'Yes' else False
    
    def get_gpu_texture_rate(row):
        rate = row[GPU_TEXTURE_RATE]
        return GPUData.extract_num_data(rate, 0, 'G')
    
    def get_gpu_vga_connection(row):
        return int(row[GPU_VGA_CONNECTION])
