import tzlocal
import csv
import pygsheets
from filepath import desktop, laptop
from statistics import mode, median
transactions = 21

# Return: number of lines in an item's CSV file
def count_lines(item):
    temp_item = item
    f_path = r'{0}\Data\{1}_history.csv'.format(laptop, temp_item)

    with open(f_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
            return line_count

def stats_twenty(item):
    total_quantity = 0
    total_cost = 0
    twenty_list = []
    temp_item = item
    lines = count_lines(item)
    f_path = r'{0}\Data\{1}_history.csv'.format(laptop, item)
    with open(f_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        parsed_data = list(csv_reader)
        for x in range(1, transactions):
            #total_quantity = total_quantity + int(parsed_data[lines-x][3])
            #twenty_list.append(int(parsed_data[lines-x][3]))
            total_cost = total_cost + int(parsed_data[lines-x][2])
        #print(f'Average Quantity over last 20: {total_quantity/20}')
        print(f'Average Price over last 20: {total_cost/20}')
        #print(f'Mode over last 20: {mode(twenty_list)}')
        #print(f'Median over last 20: {median(twenty_list)}')
        print()
    return total_cost/20
    
    # gc = pygsheets.authorize(service_file=r'{0}\editor_credentials.json'.format(laptop))
    # sh = gc.open('Market Comparison')
    # wks = sh[0]
    # print("Writing Data to Sheet")
    # wks.update_value('C2',total_cost/20)
    print("Program Exit")

def main():
    average = stats_twenty('borax')
    credential = pygsheets.authorize(service_file=r'{0}\editor_credentials.json'.format(laptop))
    sheet = credential.open('Market Comparison')
    worksheet = sheet[0] 
    cell = worksheet.find("borax")
    write_cell = cell[0].neighbour((0,2))
    write_cell.value = average



if __name__ == '__main__':
	main()