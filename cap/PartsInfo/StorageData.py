from CSVinfo import *

class StorageData:
    '''
    This class contains only static methods. Methods name are descriptive of their function.
    Additional required information, wherever necessary, has been specified.
    '''
    def get_storage_price(row):
        price = StorageData.extract_num_data(row[STORAGE_PRICES], 1, ',')
        if price == 0:
            price = StorageData.extract_num_data(row[STORAGE_PRICES], 1, ']')
        return price
    
    def get_storage_performance_score(row):
        return abs(StorageData.get_storage_cache(row) / 10) + \
        abs(StorageData.get_storage_capacity(row) / 10) + \
        StorageData.get_storage_hybrid_ssd_cache(row) + \
        (10 if StorageData.is_storage_power_loss_protection(row) else 0) + \
        (150 if StorageData.is_storage_ssd(row) else abs(StorageData.get_storage_rpm(row) / 100))

    def extract_num_data(col, start, str):
        '''
        Returns the value in 'col' as a float. The value is converted starting from the index
        'start' and ending at the index before the first occurence of 'str'.
        '''
        if str not in col:
            return 0
        return float(col[start:col.find(str)])
    
    def get_storage_cache(row):
        cache = row[STORAGE_CACHE]
        if cache == 'N/A':
            return 0
        return StorageData.extract_num_data(cache, 0, 'M')
    
    def get_storage_capacity(row):
        capacity = row[STORAGE_CAPACITY]
        if 'TB' in capacity:
            return StorageData.extract_num_data(capacity, 0, 'T') * 1000
        return StorageData.extract_num_data(capacity, 0, 'G')
    
    def get_storage_hybrid_ssd_cache(row):
        cache = row[STORAGE_HYBRID_SSD_CACHE]
        if not cache:
            return 0
        return StorageData.extract_num_data(cache, 0, 'G')
    
    def is_storage_power_loss_protection(row):
        return True if row[STORAGE_POWER_LOSS_PROTECTION] == 'Yes' else False
    
    def is_storage_ssd(row):
        return True if row[STORAGE_IS_SSD] == 'Yes' else False
    
    def get_storage_rpm(row):
        rpm = row[STORAGE_RPM]
        if not rpm:
            return 0
        return float(rpm)
