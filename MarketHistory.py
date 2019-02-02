import json
import requests
import tzlocal
import csv
from itemdict import item_dict
from apikey import api_key
from datetime import datetime
from filepath import desktop, laptop
list_size = 19

# Create new CSV for item and write the headers + first 20 transactions
def new_sheet(item):
    print('Generating New Sheet for ' + item)
    print('---------------------------------------------')
    temp_item = item.lower()
    j_data = get_data(temp_item)
    file_path = r'{0}\{1}_history.csv'.format(laptop, temp_item)
    with open(file_path, 'w+', newline='') as write_file:
        with write_file:
            fnames = ['Purchase Date - POSIX', 'Purchase Date - Day', 'Price Per Unit', 'Quantity', 'Price Total', 'Character Name']
            marketwriter = csv.DictWriter(write_file, fieldnames=fnames)    
            marketwriter.writeheader()
            for list, entry in (enumerate(reversed(j_data['History']))):
                print('Transaction', list+1, 'is new!')	
                print('Price Per Unit:', entry['PricePerUnit'])
                print('Price Total:', entry['PriceTotal'],)
                print('Quantity:', entry['Quantity'],)
                print('Purchase Date:', entry['PurchaseDate'])
                print('Character Name:', entry['CharacterName'], '\n')
                date_time = int(entry['PurchaseDate'])
                local_timezone = tzlocal.get_localzone()
                local_time = datetime.fromtimestamp(date_time, local_timezone)
                marketwriter.writerow({'Purchase Date - POSIX' : entry['PurchaseDate'], 'Purchase Date - Day' : local_time.strftime('%m/%d/%Y'), 'Price Per Unit' : entry['PricePerUnit'], 'Quantity' : entry['Quantity'], 'Price Total' : entry['PriceTotal'], 'Character Name': entry['CharacterName']})
    print()
    
# Write (new) transaction data to ongoing CSV file
# Test if any of our grabbed transactions are at a later date than our most current one in csv, and adds them to the csv
def update_sheet(item):
    print('Updating History Sheet for ' + item)
    print('---------------------------------------------')
    temp_item = item.lower()  
    j_data = get_data(temp_item)
    file_path = r'{0}\{1}_history.csv'.format(laptop, temp_item)
    
    with open (file_path,'r' ) as read_file:
        list = read_file.readlines()
        #print('The last line is:')
        #print(list[-1])
        #print('The last line time value is:')
        last_purchase = list[-1].split(',', 1)[0]
        #print(text, '\n')
        
    with open(file_path, 'a', newline='') as write_file:
        with write_file:
            fnames = ['Purchase Date - POSIX', 'Purchase Date - Day', 'Price Per Unit', 'Quantity', 'Price Total', 'Character Name']
            marketwriter = csv.DictWriter(write_file, fieldnames=fnames)    
            #marketwriter.writeheader()
            for list, entry in (enumerate(reversed(j_data['History']))):
                if entry['PurchaseDate'] > int(last_purchase):
                    print('Transaction:', list+1, 'is new!')	
                    print('Price Per Unit:', entry['PricePerUnit'])
                    print('Price Total:', entry['PriceTotal'],)
                    print('Quantity:', entry['Quantity'],)
                    print('Purchase Date:', entry['PurchaseDate'],)
                    print('Character Name:', entry['CharacterName'], '\n')
                    date_time = int(entry['PurchaseDate'])
                    local_timezone = tzlocal.get_localzone()
                    local_time = datetime.fromtimestamp(date_time, local_timezone)
                    marketwriter.writerow({'Purchase Date - POSIX' : entry['PurchaseDate'], 'Purchase Date - Day' : local_time.strftime('%m/%d/%Y'), 'Price Per Unit' : entry['PricePerUnit'], 'Quantity' : entry['Quantity'], 'Price Total' : entry['PriceTotal'], 'Character Name': entry['CharacterName']})
                else:
                    if list == list_size:
                        print('No New Transactions')
    print()

#def update_gsheet(item):

# Return: JSON transaction data for input item
def get_data(item):
    temp_item = item.lower()
    file_path = r'{0}\{1}_history.json'.format(laptop, temp_item)
    j_path = 'https://xivapi.com/market/adamantoise/items/{0}/history?key={1}&columns=History.*19.PricePerUnit,History.*19.PriceTotal,History.*19.PurchaseDate,History.*19.Quantity,History.*19.CharacterName'.format(item_dict[temp_item], api_key)
    response = requests.get(j_path)
    data = response.json()
    with open(file_path, 'w+') as write_file:
        json.dump(data, write_file)
    return data;

def main():
    for key in item_dict.keys():
        update_sheet(key)
        #update_gsheet(key)

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