#{REQ-1}
from sys import argv, exit
import os
from datetime import date

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

def get_dir(get_sales):

    sales_dir = os.path.dirname(sales_csv)

    tdate = date.today.isoformat()
   
    odir = os.path.join(sales_dir, 'Orders_ ' + tdate)

get_sales = sales_csv()
order_dir = get_dir(get_sales)

