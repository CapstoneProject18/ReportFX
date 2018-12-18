#!/usr/bin/python3
import unittest
from CPUData         import *
from CSVinfo         import *
from GPUData         import *
from MemoryData      import *
from MotherboardData import *
from StorageData     import *

CPU_ROW = ['4th Generation Intel® Core™ i7 Processors', 'i7-4790S', 'Q2 2014', '22 nm', \
            '$303.00 - $312.00', '4', '8', '3.20 GHz', '4.00 GHz', '8 MB SmartCache', '65 W', \
            '32 GB', 'DDR3-1333/1600, DDR3L-1333/1600 @ 1.5V', '2', '25.6 GB/s', 'No', \
            '350 MHz', '1.20 GHz', '2 GB', 'eDP/DP/HDMI/DVI/VGA', '', '4096x2304@24Hz', \
            '3840x2160@60Hz', '3840x2160@60Hz', '11.2/12', '', 'Up to 3.0', \
            'Up to 1x16, 2x8, 1x8+2x4', '16', '71.35°C', 'Yes', 'SSE4.1/4.2, AVX 2.0', 'Yes', \
            'Yes', 'Yes', 'LGA1150']
GPU_ROW = ['Pascal P107', '1920 x 1080', '1392 MHz', '1290 MHz', '1', 'DX 12.1', '1', '1', \
            '1024KB', 'Nvidia', '75 Watts', '4096 MB', '112.1GB/sec', '128 Bit', '1752 MHz', \
            'GDDR5', 'GeForce GTX 1050 Ti PNY 4GB', '4.5', '300 Watt & 27 Amps', '45 GPixel/s', \
            '16nm', '$150.00', '7680x4320', 'No', '5', '67 GTexel/s', '0', 'Q3 2014']
MEMORY_ROW = ['9', 'No', 'Yes', 'Corsair', 'Corsair XMS3 4GB (2 x 2GB) DDR3-1333 Memory', \
                '$11.25', '[44.99]', '4GB (2 x 2GB)', 'DDR3-1333', 'False', '1333', '', '1333', \
                'Q3 2006']
MOTHERBOARD_ROW = ['LGA1151', 'Intel C236', 'No', 'ATX', 'Asus', '64GB', 'DDR4-2133', \
                    'Asus P10S-E/4L ATX LGA1151 Motherboard', '4 x 10/100/1000 Mbps', 'Yes', \
                    'Yes', '[289.0, 291.99]', 'Yes', 'No', 'Q3 2015']
STORAGE_ROW = ['16MB', '500GB', '', 'Hitachi', \
                'Hitachi Travelstar 500GB 2.5" 7200RPM Internal Hard Drive', '', '$0.12', \
                '[52.99]', '7200', 'No']

class TestPartsInfo(unittest.TestCase):

    #==============
    # TEST CPUData
    #==============

    def test_get_cpu_price(self):
        expected_value = 303.0
        self.assertEqual(CPUData.get_cpu_price(CPU_ROW), expected_value)
    
    def test_get_cpu_performance_score(self):
        expected_value = 289
        self.assertEqual(int(CPUData.get_cpu_performance_score(CPU_ROW)), expected_value)
    
    def test_get_cpu_lithography(self):
        expected_value = 22.0
        self.assertEqual(CPUData.get_cpu_lithography(CPU_ROW), expected_value)
    
    def test_get_cpu_base_frequency(self):
        expected_value = 3.2
        self.assertEqual(CPUData.get_cpu_base_frequency(CPU_ROW), expected_value)
    
    def test_get_cpu_turbo_frequency(self):
        expected_value = 4.0
        self.assertEqual(CPUData.get_cpu_turbo_frequency(CPU_ROW), expected_value)
    
    def test_get_cpu_cache(self):
        expected_value = 8.0
        self.assertEqual(CPUData.get_cpu_cache(CPU_ROW), expected_value)
    
    def test_get_cpu_tdp(self):
        expected_value = 65.0
        self.assertEqual(CPUData.get_cpu_tdp(CPU_ROW), expected_value)
    
    def test_get_cpu_max_memory(self):
        expected_value = 32.0
        self.assertEqual(CPUData.get_cpu_max_memory(CPU_ROW), expected_value)
    
    def test_get_cpu_mem_channels(self):
        expected_value = 2
        self.assertEqual(CPUData.get_cpu_mem_channels(CPU_ROW), expected_value)
    
    def test_get_cpu_max_memory_bandwidth(self):
        expected_value = 25.6
        self.assertEqual(CPUData.get_cpu_max_memory_bandwidth(CPU_ROW), expected_value)
    
    def test_cpu_is_ecc_supported(self):
        expected_value = False
        self.assertEqual(CPUData.cpu_is_ecc_supported(CPU_ROW), expected_value)
    
    def test_get_cpu_graphics_base_freq(self):
        expected_value = 350.0
        self.assertEqual(CPUData.get_cpu_graphics_base_freq(CPU_ROW), expected_value)
    
    def test_get_cpu_graphics_max_freq(self):
        expected_value = 1.2
        self.assertEqual(CPUData.get_cpu_graphics_max_freq(CPU_ROW), expected_value)
    
    def test_get_cpu_graphics_max_mem(self):
        expected_value = 2.0
        self.assertEqual(CPUData.get_cpu_graphics_max_mem(CPU_ROW), expected_value)
    
    def test_get_cpu_T(self):
        expected_value = 71.35
        self.assertEqual(CPUData.get_cpu_T(CPU_ROW), expected_value)
    
    def test_cpu_is_ht_supported(self):
        expected_value = True
        self.assertEqual(CPUData.cpu_is_ht_supported(CPU_ROW), expected_value)
    
    def test_cpu_is_secure_key_supported(self):
        expected_value = True
        self.assertEqual(CPUData.cpu_is_secure_key_supported(CPU_ROW), expected_value)
    
    def test_get_cpu_no_of_cores(self):
        expected_value = 4
        self.assertEqual(CPUData.get_cpu_no_of_cores(CPU_ROW), expected_value)
    
    def test_get_no_of_thread(self):
        expected_value = 8
        self.assertEqual(CPUData.get_no_of_thread(CPU_ROW), expected_value)
    
    #==============
    # TEST GPUData
    #==============
    
    def test_get_gpu_price(self):
        expected_value = 150.0
        self.assertEqual(GPUData.get_gpu_price(GPU_ROW), expected_value)
    
    def test_get_gpu_performance_score(self):
        expected_value = 375
        self.assertEqual(int(GPUData.get_gpu_performance_score(GPU_ROW)), expected_value)
    
    def test_get_gpu_boost_clock(self):
        expected_value = 1392.0
        self.assertEqual(GPUData.get_gpu_boost_clock(GPU_ROW), expected_value)
    
    def test_get_gpu_core_speed(self):
        expected_value = 1290.0
        self.assertEqual(GPUData.get_gpu_core_speed(GPU_ROW), expected_value)
    
    def test_get_gpu_dvi_connection(self):
        expected_value = 1
        self.assertEqual(GPUData.get_gpu_dvi_connection(GPU_ROW), expected_value)
    
    def test_get_gpu_hdmi_connection(self):
        expected_value = 1
        self.assertEqual(GPUData.get_gpu_hdmi_connection(GPU_ROW), expected_value)
    
    def test_get_gpu_l2_cache(self):
        expected_value = 1024.0
        self.assertEqual(GPUData.get_gpu_l2_cache(GPU_ROW), expected_value)
    
    def test_get_gpu_max_power(self):
        expected_value = 75.0
        self.assertEqual(GPUData.get_gpu_max_power(GPU_ROW), expected_value)
    
    def test_get_gpu_memory(self):
        expected_value = 4096.0
        self.assertEqual(GPUData.get_gpu_memory(GPU_ROW), expected_value)
    
    def test_get_gpu_memory_bandwidth(self):
        expected_value = 112.1
        self.assertEqual(GPUData.get_gpu_memory_bandwidth(GPU_ROW), expected_value)
    
    def test_get_gpu_memory_speed(self):
        expected_value = 1752.0
        self.assertEqual(GPUData.get_gpu_memory_speed(GPU_ROW), expected_value)
    
    def test_get_gpu_memory_type_score(self):
        expected_value = 20
        self.assertEqual(GPUData.get_gpu_memory_type_score(GPU_ROW), expected_value)
    
    def test_get_gpu_pixel_rate(self):
        expected_value = 45.0
        self.assertEqual(GPUData.get_gpu_pixel_rate(GPU_ROW), expected_value)
    
    def test_get_gpu_process(self):
        expected_value = 16.0
        self.assertEqual(GPUData.get_gpu_process(GPU_ROW), expected_value)
    
    def test_is_gpu_sli_crossfire_supported(self):
        expected_value = False
        self.assertEqual(GPUData.is_gpu_sli_crossfire_supported(GPU_ROW), expected_value)
    
    def test_get_gpu_texture_rate(self):
        expected_value = 67.0
        self.assertEqual(GPUData.get_gpu_texture_rate(GPU_ROW), expected_value)
    
    def test_get_gpu_vga_connection(self):
        expected_value = 0
        self.assertEqual(GPUData.get_gpu_vga_connection(GPU_ROW), expected_value)
    
    #=================
    # TEST MemoryData
    #=================
    
    def test_get_memory_price(self):
        expected_value = 44.99
        self.assertEqual(MemoryData.get_memory_price(MEMORY_ROW), expected_value)
    
    def test_get_memory_performance_score(self):
        expected_value = 52
        self.assertEqual(int(MemoryData.get_memory_performance_score(MEMORY_ROW)), expected_value)
    
    def test_get_memory_cas_latency(self):
        expected_value = 9.0
        self.assertEqual(MemoryData.get_memory_cas_latency(MEMORY_ROW), expected_value)
    
    def test_is_memory_ecc_supported(self):
        expected_value = False
        self.assertEqual(MemoryData.is_memory_ecc_supported(MEMORY_ROW), expected_value)
    
    def test_is_memory_heat_spreader_supported(self):
        expected_value = True
        self.assertEqual(MemoryData.is_memory_heat_spreader_supported(MEMORY_ROW), expected_value)
    
    def test_get_memory_size(self):
        expected_value = 4.0
        self.assertEqual(MemoryData.get_memory_size(MEMORY_ROW), expected_value)
    
    def test_is_memory_ddr4(self):
        expected_value = False
        self.assertEqual(MemoryData.is_memory_ddr4(MEMORY_ROW), expected_value)
    
    def test_get_memory_ddr3_speed(self):
        expected_value = 1333.0
        self.assertEqual(MemoryData.get_memory_ddr3_speed(MEMORY_ROW), expected_value)
    
    def test_get_memory_ddr4_speed(self):
        with self.assertRaises(ValueError):
            expected_value = MemoryData.get_memory_ddr4_speed(MEMORY_ROW)
    
    def test_get_memory_speed(self):
        expected_value = 1333.0
        self.assertEqual(MemoryData.get_memory_speed(MEMORY_ROW), expected_value)
    
    def test_get_memory_name(self):
        expected_value = 'Corsair XMS3 4GB (2 x 2GB) DDR3-1333 Memory'
        self.assertEqual(MemoryData.get_memory_name(MEMORY_ROW), expected_value)
    
    #======================
    # TEST MotherboardData
    #======================
    
    def test_get_motherboard_price(self):
        expected_value = 289.0
        self.assertEqual(MotherboardData.get_motherboard_price(MOTHERBOARD_ROW), expected_value)
    
    def test_get_motherboard_performance_score(self):
        expected_value = 150
        self.assertEqual(MotherboardData.get_motherboard_performance_score(MOTHERBOARD_ROW), expected_value)
    
    def test_get_motherboard_ethernet_score(self):
        expected_value = 100
        self.assertEqual(MotherboardData.get_motherboard_ethernet_score(MOTHERBOARD_ROW), expected_value)
    
    def test_is_motherboard_usb3_header(self):
        expected_value = True
        self.assertEqual(MotherboardData.is_motherboard_usb3_header(MOTHERBOARD_ROW), expected_value)
    
    #==================
    # TEST StorageData
    #==================

    def test_get_storage_price(self):
        expected_value = 52.99
        self.assertEqual(StorageData.get_storage_price(STORAGE_ROW), expected_value)
    
    def test_get_storage_performance_score(self):
        expected_value = 123
        self.assertEqual(int(StorageData.get_storage_performance_score(STORAGE_ROW)), expected_value)
    
    def test_get_storage_cache(self):
        expected_value = 16.0
        self.assertEqual(StorageData.get_storage_cache(STORAGE_ROW), expected_value)
    
    def test_get_storage_capacity(self):
        expected_value = 500.0
        self.assertEqual(StorageData.get_storage_capacity(STORAGE_ROW), expected_value)
    
    def test_get_storage_hybrid_ssd_cache(self):
        expected_value = 0
        self.assertEqual(StorageData.get_storage_hybrid_ssd_cache(STORAGE_ROW), expected_value)
    
    def test_is_storage_power_loss_protection(self):
        expected_value = False
        self.assertEqual(StorageData.is_storage_power_loss_protection(STORAGE_ROW), expected_value)
    
    def test_is_storage_ssd(self):
        expected_value = False
        self.assertEqual(StorageData.is_storage_ssd(STORAGE_ROW), expected_value)
    
    def test_get_storage_rpm(self):
        expected_value = 7200.0
        self.assertEqual(StorageData.get_storage_rpm(STORAGE_ROW), expected_value)

if __name__ == '__main__':
    unittest.main()
