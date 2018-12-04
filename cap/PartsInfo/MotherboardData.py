from CSVinfo import *

class MotherboardData:
    '''
    This class contains only static methods. Methods name are descriptive of their function.
    Additional required information, wherever necessary, has been specified.
    '''
    def get_motherboard_price(row):
        price = MotherboardData.extract_num_data(row[MOTHERBOARD_PRICES], 1, ',')
        if price == 0:
            price = MotherboardData.extract_num_data(row[MOTHERBOARD_PRICES], 1, ']')
        return price
    
    def get_motherboard_performance_score(row):
        return MotherboardData.get_motherboard_ethernet_score(row) + \
        (50 if MotherboardData.is_motherboard_usb3_header(row) else 0)

    def extract_num_data(col, start, str):
        '''
        Returns the value in 'col' as a float. The value is converted starting from the index
        'start' and ending at the index before the first occurence of 'str'.
        '''
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
