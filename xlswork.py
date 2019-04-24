#!/usr/bin/python3

import xlrd
import xlwt
import re

workbook=xlrd.open_workbook(r'D:\OneDrive\python\LQL-SAEGW_test_case_list_v1.1_stream495_DPI_20190422.xls')
#print (workbook.sheet_names())

bugsheet=workbook.sheet_by_name('Bug Statistics')
#print (bugsheet.name,bugsheet.nrows,bugsheet.ncols)
cols=bugsheet.col_values(6)
#print (cols)

l1=len(cols) 
print (l1)
#for i in range (l1):
#    print (bugsheet.cell(6,i))