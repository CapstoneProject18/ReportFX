from CSVinfo import *

class MotherboardData:
    def get_motherboard_price(row):
        return MotherboardData.extract_num_data(row[MOTHERBOARD_PRICES], 1, ',')
    
    def get_motherboard_performance_score(row):
        return MotherboardData.get_motherboard_ethernet_score(row) + \
        (50 if MotherboardData.is_motherboard_usb3_header(row) else 0)

    def extract_num_data(col, start, str):
        if str not in col:
            return 0
        return float(col[start:col.find(str)])
    
    def get_motherboard_ethernet_score(row):
        ethernet = row[MOTHERBOARD_ONBOARD_ETHERNET]
        multiplier = int(ethernet[0])

        if 'Gbps' in ethernet:
            return 50 * multiplier
        
        return 25 * multiplier
    
    def is_motherboard_usb3_header(row):
        return True if row[MOTHERBOARD_ONBOARD_USB3] == 'Yes' else False
