import tzlocal
import csv
import pygsheets
#import sqlite3
from filepath import desktop, laptop
from statistics import mode, median

def count_lines(item):
    temp_item = item
    f_path = r'{0}\{1}_history.csv'.format(desktop, temp_item)

    with open(f_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    #print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    #print(f'\t Posix Time: {row[0]} Date: {row[1]} PPU: {row[2]} Quantity: {row[3]} Total: {row[4]} Name: {row[5]}')
                    #total_quantity = total_quantity + int(row[3])
                    line_count += 1
            #print(f'Processed {line_count} lines.')
            return line_count
            #print(f'Total Quantity sold:{total_quantity}')
            #print(f'Average Quantity sold per transaction:{total_quantity/line_count}')

def stats_twenty(item):
    total_quantity = 0
    total_cost = 0
    twenty_list = []
    temp_item = item
    lines = count_lines(item)
    f_path = r'{0}\{1}_history.csv'.format(desktop, 'borax')
    with open(f_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        parsed_data = list(csv_reader)
        for x in range(1, 21):
            #print(parsed_data[lines-x][3] + f' Count: {x}')
            total_quantity = total_quantity + int(parsed_data[lines-x][3])
            twenty_list.append(int(parsed_data[lines-x][3]))
            total_cost = total_cost + int(parsed_data[lines-x][2])
        print(f'Average Quantity over last 20: {total_quantity/20}')
        print(f'Average Price over last 20: {total_cost/20}')
        print(f'Mode over last 20: {mode(twenty_list)}')
        print(f'Median over last 20: {median(twenty_list)}')

    gc = pygsheets.authorize(service_file=r'{0}\editor_credentials.json'.format(desktop))
    #open the google spreadsheet 
    sh = gc.open('Market Comparison')
    wks = sh[0]
    #update the first sheet with df, starting at cell B2. 
    print("Writing Data to Sheet")
    wks.update_value('C2',total_cost/20)
    print("Program Exit")

def main():
    stats_twenty('borax')



if __name__ == '__main__':
	main()