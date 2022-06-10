import re
from sys import argv, exit
import os
from datetime import date
from openpyxl import Workbook
import pandas as pd
import numpy as np
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

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

    sales_dir = os.path.dirname(get_sales) 

    tdate = date.today().isoformat()
    fdate = 'Orders_ ' + tdate
   
    odir = os.path.join(sales_dir, fdate)

    if not os.path.exists(odir):
        os.makedirs(odir)

    return odir

def split_sales(get_sales, order_dir):

    sales_df = pd.read_csv(get_sales)

    sales_df.insert(7, 'TOTAL PRICE', sales_df['ITEM QUANTITY'] * sales_df['ITEM PRICE'])

    sales_df.drop(columns=['ADDRESS', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY'], inplace=True)

    for order_id, order_df in sales_df.groupby('ORDER ID'):

        order_df.drop(columns=['ORDER ID'], inplace=True)

        order_df.sort_values(by='ITEM NUMBER', inplace=True)

        grand_total = order_df['TOTAL PRICE'].sum()
        grand_total_df = pd.DataFrame({'ITEM PRICE' : ['GRAND TOTAL:'], 'TOTAL PRICE' : [grand_total]})
        order_df = pd.concat([order_df, grand_total_df])

        customer_name = order_df['CUSTOMER NAME'].values[0] 
        customer_name = re.sub(r'\W', '', customer_name)
        order_file_name ='Order' + str(order_id) +'_' + customer_name + '.xlsx' 
        order_file_path = os.path.join(order_dir, order_file_name)

        sheet_name = 'Order #' + str(order_id)

        writer = pd.ExcelWriter(order_file_path,engine='xlsxwriter')
        order_df.to_excel(writer, index=False , sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        number_col = len(order_df.index)
        price_fmt = workbook.add_format({'num_format' :  '$#,####.00', 'bold': True})
        color_range = "F1:G6".format(number_col)
        format1 = workbook.add_format({'bg_color': '#fffac7'})
        worksheet.conditional_format(color_range, {'type': 'top','value': '#','format': format1})
        worksheet.set_column('A:E', 15)
        worksheet.set_column('F:G', 15, price_fmt)
        worksheet.set_column('H:H', 15)
        worksheet.set_column('I:I', 26)

        writer.save()
        #order_df.to_excel(order_file_path, index=False, sheet_name=sheet_name)

get_sales = sales_csv()
order_dir = get_dir(get_sales)
split_sales(get_sales, order_dir)

