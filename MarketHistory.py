import json
import requests
import tzlocal
import csv
from datetime import datetime

def main():

	print('Running Borax History Test\n')
	#Grab our JSON with transaction data for last 20 transactions
	b_response = requests.get('https://xivapi.com/market/adamantoise/items/9366/history?key=0eb7d823c3c94be0a1bb01be&columns=History.*19.PricePerUnit,History.*19.PriceTotal,History.*19.PurchaseDate,History.*19.Quantity')
	b_data = b_response.json()
	
	#Dump JSON data to local file
	with open(r'C:\Users\gogge\Documents\GitHub\FFXIV-market-history\borax_history.json', 'w+') as write_file:
		json.dump(b_data, write_file)
	
	#Write (new) transaction data to ongoing CSV file
	with open(r'C:\Users\gogge\Documents\GitHub\FFXIV-market-history\borax_history.csv', 'w+', newline='') as f:
		with f:
			fnames = ['Purchase Date', 'Price Per Unit', 'Quantity', 'Price Total']
			marketwriter = csv.DictWriter(f, fieldnames=fnames)    
			marketwriter.writeheader()
			for list, entry in (enumerate(reversed(b_data['History']))):
				print('Transaction', list+1)
				print('Price Per Unit', entry['PricePerUnit'])
				print('Price Total', entry['PriceTotal'],)
				print('Quantity', entry['Quantity'],)
				print('Purchase Date', entry['PurchaseDate'], '\n')
				marketwriter.writerow({'Purchase Date' : entry['PurchaseDate'], 'Price Per Unit' : entry['PricePerUnit'], 'Quantity' : entry['Quantity'], 'Price Total' : entry['PriceTotal']})
	
	# read a text file as a list of lines
	# find the last line, print it
	# lazy implementation to find last line (will be s l o w on larger files, but works for us to read whole file into memory)
	with open (r'C:\Users\gogge\Documents\GitHub\FFXIV-market-history\borax_history.csv','r' ) as f:
		list = f.readlines()
		print('The last line is:')
		print(list[-1])
	
	print('Running UNIX Time Conversion Test On First Transaction', '\n')
	dict = b_data['History'][0]
	test_time = int(dict['PurchaseDate'])
	print('POSIX Time:', test_time)
	local_timezone = tzlocal.get_localzone()
	local_time = datetime.fromtimestamp(test_time, local_timezone)
	
	print('Local Time (Date):', local_time.strftime('%m/%d/%Y'))
	print('Local Time (Time):', local_time.strftime('%H:%M:%S'))
	
	print()
	

	
	print('\nProgram Exit')
	
	
if __name__ == '__main__':
	main()