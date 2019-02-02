import json
import requests
import tzlocal
import csv
from itemdict import item_dict
from apikey import api_key
from datetime import datetime
from filepath import desktop, laptop
list_size = 19

# Create new CSV for item and write the headers + last 20 sales
def new_sheet(item):
    print('Generating New Sheet for ' + item)
    print('---------------------------------------------')
    temp_item = item.lower()
    json_data = get_data(temp_item)
    file_path = r'{0}\{1}_history.csv'.format(laptop, temp_item)
    with open(file_path, 'w+', newline='') as write_file:
        with write_file:
            fnames = ['Purchase Date - POSIX', 'Purchase Date - Day', 'Price Per Unit', 'Quantity', 'Price Total', 'Character Name']
            marketwriter = csv.DictWriter(write_file, fieldnames=fnames)    
            marketwriter.writeheader()
            for transaction, data in (enumerate(reversed(json_data['History']))):
                add_transaction(transaction, data, write_file)
    print()
    
# Update CSV for specified item with any new item sales
def update_sheet(item):
    print('Updating History Sheet for ' + item)
    print('---------------------------------------------')
    temp_item = item.lower()  
    json_data = get_data(temp_item)
    file_path = r'{0}\{1}_history.csv'.format(laptop, temp_item)
    
    with open (file_path,'r' ) as read_file:
        list = read_file.readlines()
        last_purchase = list[-1].split(',', 1)[0]
        
    with open(file_path, 'a', newline='') as write_file:
        with write_file:  
            for transaction, data in (enumerate(reversed(json_data['History']))):
                if data['PurchaseDate'] > int(last_purchase):
                    add_transaction(transaction, data, write_file)
                elif transaction == list_size:
                    print('No New Transactions')
    print()

#def update_gsheet(item):

# Return: JSON transaction data for specified item
def get_data(item):
    temp_item = item.lower()
    file_path = r'{0}\{1}_history.json'.format(laptop, temp_item)
    json_request = 'https://xivapi.com/market/adamantoise/items/{0}/history?key={1}&columns=History.*19.PricePerUnit,History.*19.PriceTotal,History.*19.PurchaseDate,History.*19.Quantity,History.*19.CharacterName'.format(item_dict[temp_item], api_key)
    response = requests.get(json_request)
    data = response.json()
    with open(file_path, 'w+') as write_file:
        json.dump(data, write_file)
    return data;

# Write a single transaction to specified CSV file
def add_transaction(number, data, write_file):
    fnames = ['Purchase Date - POSIX', 'Purchase Date - Day', 'Price Per Unit', 'Quantity', 'Price Total', 'Character Name']
    marketwriter = csv.DictWriter(write_file, fieldnames=fnames)  
    print('Transaction:', number+1, 'is new!')	
    print('Price Per Unit:', data['PricePerUnit'])
    print('Price Total:', data['PriceTotal'],)
    print('Quantity:', data['Quantity'],)
    print('Purchase Date:', data['PurchaseDate'],)
    print('Character Name:', data['CharacterName'], '\n')
    date_time = int(data['PurchaseDate'])
    local_timezone = tzlocal.get_localzone()
    local_time = datetime.fromtimestamp(date_time, local_timezone)
    marketwriter.writerow({'Purchase Date - POSIX' : data['PurchaseDate'], 'Purchase Date - Day' : local_time.strftime('%m/%d/%Y'), 'Price Per Unit' : data['PricePerUnit'], 'Quantity' : data['Quantity'], 'Price Total' : data['PriceTotal'], 'Character Name': data['CharacterName']})
            
def main():
    for key in item_dict.keys():
        update_sheet(key)
        #update_gsheet(key)
    print('\nProgram Exit')
	
if __name__ == '__main__':
	main()