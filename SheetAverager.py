import tzlocal
import csv
from filepath import desktop, laptop

def main():
    temp_item = 'borax'
    f_path = r'{0}\{1}_history.csv'.format(desktop, temp_item)
    total_quantity = 0

    with open(f_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} Posix Time {row[1]} Date {row[2]} PPU {row[3]} Quantity {row[4]} Total {row[5]} Name.')
                total_quantity = total_quantity + int(row[4])
                line_count += 1
        print(f'Processed {line_count} lines.')
        print(f'Total Quantity sold:{total_quantity}')
        print(f'Average Quantity sold per transaction:{total_quantity/line_count}')

if __name__ == '__main__':
	main()