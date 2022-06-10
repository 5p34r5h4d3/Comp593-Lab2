#{REQ-1}
from multiprocessing import reduction
from sys import argv, exit
import os

def sales_csv():

    if len(argv) >= 2:
        csv_file = argv[1]

        if os.path.isfile(csv_file):
            return csv_file
        else:
            print("File not found")
            exit("Exiting script")        
    else:
        print("No path found")
        exit("Exiting script")

get_sales = sales_csv()
print(get_sales)

