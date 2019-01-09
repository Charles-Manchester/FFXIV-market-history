import json
import requests
import tzlocal
import csv
from itemdict import item_dict
from apikey import api_key
from datetime import datetime
from filepath import desktop, laptop

# Method that takes item name as input, grabs it's JSON data and writes to a local file. item names not in dict are rejected, see itemdict.py for acceptable items
# Return: JSON transaction data for input item
def get_data(item):
    temp_item = item.lower()
    f_request = None
    f_path = r'{0}\{1}_history.json'.format(laptop, temp_item)
    j_path = 'https://xivapi.com/market/adamantoise/items/{0}/history?key={1}&columns=History.*19.PricePerUnit,History.*19.PriceTotal,History.*19.PurchaseDate,History.*19.Quantity'.format(item_dict[temp_item], api_key)
    response = requests.get(j_path)
    data = response.json()
    with open(f_path, 'w+') as write_file:
        json.dump(data, write_file)
    return data;

# Create new CSV for item and write the headers + first 20 transactions
def new_sheet(item):
    temp_item = item.lower()
    j_data = get_data(temp_item)
    f_path = r'{0}\{1}_history.csv'.format(laptop, temp_item)
    with open(f_path, 'w+', newline='') as write_file:
        with write_file:
            fnames = ['Purchase Date - POSIX', 'Purchase Date - Day', 'Price Per Unit', 'Quantity', 'Price Total']
            marketwriter = csv.DictWriter(write_file, fieldnames=fnames)    
            marketwriter.writeheader()
            for list, entry in (enumerate(reversed(j_data['History']))):
                print('Transaction', list+1, 'is new!')	
                print('Price Per Unit', entry['PricePerUnit'])
                print('Price Total', entry['PriceTotal'],)
                print('Quantity', entry['Quantity'],)
                print('Purchase Date', entry['PurchaseDate'], '\n')
                date_time = int(entry['PurchaseDate'])
                local_timezone = tzlocal.get_localzone()
                local_time = datetime.fromtimestamp(date_time, local_timezone)
                marketwriter.writerow({'Purchase Date - POSIX' : entry['PurchaseDate'], 'Purchase Date - Day' : local_time.strftime('%m/%d/%Y'), 'Price Per Unit' : entry['PricePerUnit'], 'Quantity' : entry['Quantity'], 'Price Total' : entry['PriceTotal']})

# Write (new) transaction data to ongoing CSV file
# Test if any of our grabbed transactions are at a later date than our most current one in csv, and adds them to the csv
def update_sheet(item):
    temp_item = item.lower()  
    j_data = get_data(temp_item)
    f_path = r'{0}\{1}_history.csv'.format(laptop, temp_item)
    
    with open (f_path,'r' ) as read_file:
        list = read_file.readlines()
        print('The last line is:')
        print(list[-1])
        print('The last line time value is:')
        text = list[-1].split(',', 1)[0]
        print(text, '\n')
        
    with open(f_path, 'a', newline='') as write_file:
        with write_file:
            fnames = ['Purchase Date - POSIX', 'Purchase Date - Day', 'Price Per Unit', 'Quantity', 'Price Total']
            marketwriter = csv.DictWriter(write_file, fieldnames=fnames)    
            #marketwriter.writeheader()
            for list, entry in (enumerate(reversed(j_data['History']))):
                if entry['PurchaseDate'] > int(text):
                    print('Transaction', list+1, 'is new!')	
                    print('Price Per Unit', entry['PricePerUnit'])
                    print('Price Total', entry['PriceTotal'],)
                    print('Quantity', entry['Quantity'],)
                    print('Purchase Date', entry['PurchaseDate'], '\n')
                    date_time = int(entry['PurchaseDate'])
                    local_timezone = tzlocal.get_localzone()
                    local_time = datetime.fromtimestamp(date_time, local_timezone)
                    marketwriter.writerow({'Purchase Date - POSIX' : entry['PurchaseDate'], 'Purchase Date - Day' : local_time.strftime('%m/%d/%Y'), 'Price Per Unit' : entry['PricePerUnit'], 'Quantity' : entry['Quantity'], 'Price Total' : entry['PriceTotal']})
                else:
                    print('Transcation', list+1, 'from JSON is already processed')
        
def main():
    print('Running Borax History Test\n')
    update_sheet('Borax')

    # print('Running UNIX Time Conversion Test On First Transaction', '\n')
    # dict = b_data['History'][0]
    # test_time = int(dict['PurchaseDate'])
    # print('POSIX Time:', test_time)
    # local_timezone = tzlocal.get_localzone()
    # local_time = datetime.fromtimestamp(test_time, local_timezone)

    # print('Local Time (Date):', local_time.strftime('%m/%d/%Y'))
    # print('Local Time (Time):', local_time.strftime('%H:%M:%S'))

    # print()

    print('\nProgram Exit')
	
if __name__ == '__main__':
	main()