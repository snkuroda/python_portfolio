"""
Title: Election Results by County

Description: Pulls 2016 Presidential data by county from Wikipedia,
and creates a csv.
"""

import arcpy, urllib2, os, csv, re
import numpy as np
from bs4 import BeautifulSoup as BS

# Set inputs
csv_file = r"E:\GIS_DATA\GEO_242\Final_Project\ElectionResultAnalysis\St_Elections.txt"
counties = r"E:\GIS_DATA\US_BOUNDARY\cb_2016_us_county_500k.shp"

### Parse individual states to url path

state_elec_csv = csv.reader(open(csv_file), delimiter = '\t')
state_elec_csv.next() #Skip header

# Lexicon for header names
trump_headers = ['Trump', 'Trump#', 'Trump votes', 'Trump Votes']
clinton_headers = ['Clinton', 'Clinton#', 'Clinton votes', 'Clinton Votes']
johnson_headers = ['Johnson', 'Johnson#', 'Johnson Votes']
stein_headers = ['Stein', 'Stein#', 'Stein Votes']
total_headers = ['Total', 'Totals', 'Total Votes', 'Totals#']
other_headers = ['Other#', "Other", "Other votes", 'Others']

for state in state_elec_csv:
    
    
    if state[2]== 'wikisort':
        print(state[0])
        url = state[-1] # url of the wiki page pulled from csv
        header = {'User-Agent': 'Mozilla/5.0'}
        request = urllib2.Request(url, headers=header)
        page = urllib2.urlopen(request)
        soup = BS(page, "html.parser")

        state_results = []
                
        
        header_list = []
        print(len(soup.findAll('table', class_= 'wikitable sortable')))
        
        # If there is only one sortable wikitable
        if len(soup.findAll('table', class_= 'wikitable sortable')) == 1:
            table = soup.find('table', class_= 'wikitable sortable')
            for row in table.findAll('tr')[:1]:
                ### Determine Header indexes
                for header in row.findAll('th'):
                    # Checks for b tag in html
                    if header.b is not None:
                        header_list.append(header.b.contents[0])    
                    # Passes if there no b tag
                    else:    
                        header_list.append(header.contents[0])
                

            # Assign set index number to text
            for header in header_list:
                # Checks for matching names, since some tables use slightly different header names
                find_t_index = list(set(trump_headers).intersection(header_list))[0]
                find_c_index = list(set(clinton_headers).intersection(header_list))[0]
                try:
                    find_total_index = list(set(total_headers).intersection(header_list))[0]
                    Total_index = header_list.index(find_total_index)
                except:
                    Total_index = -9999
                try:
                    find_s_index = list(set(stein_headers).intersection(header_list))[0]
                    Stein_index = header_list.index(find_s_index)
                except:
                    Stein_index = -9999
                try:
                    find_j_index = list(set(johnson_headers).intersection(header_list))[0]
                    Johnson_index = header_list.index(find_j_index)
                except:
                    Johnson_index = -9999
                try:
                    find_o_index = list(set(other_headers).intersection(header_list))[0]
                    Other_index = header_list.index(find_o_index)
                except:
                    Other_index = -9999

            # Sets index number
            Trump_index = header_list.index(find_t_index)
            Clinton_index = header_list.index(find_c_index)

            if state[0] == 'Kentucky' or state[0] == 'North Carolina':
                for row in table.findAll('tr')[1:-1]:
                    cells = row.findAll('td')
                    
                    try:
                        County = cells[0].a.contents[0]
                    except:
                        County = cells[0].contents[0]

            
                    try:
                        Trump = int(cells[Trump_index].b.contents[0].replace(',',''))
                    except:
                        Trump = int(cells[Trump_index].contents[0].replace(',',''))
                    try:
                        Clinton = int(cells[Clinton_index].b.contents[0].replace(',',''))
                    except:
                        Clinton = int(cells[Clinton_index].contents[0].replace(',',''))

                    if Johnson_index != -9999:
                        Johnson = int(cells[Johnson_index].contents[0].replace(',',''))
                    elif Johnson_index == -9999:
                        Johnson = 0
                    if Stein_index != -9999: 
                        Stein = int(cells[Stein_index].contents[0].replace(',',''))
                    elif Stein_index == -9999:
                        Stein = 0
                     
                    try:
                        if Other_index != -9999: 
                                Other = int(cells[Other_index].contents[0].replace(',',''))
                                
                        elif Other_index == -9999:
                                Other = int(cells[Total_index].contents[0].replace(',','')) - (Trump + Clinton + Johnson + Stein)
                    except:
                        Other = 0
                        
                    co_rows = [County, Clinton, Trump, Johnson, Stein, Other]

                    state_results.append(co_rows)

            
            else:        
                for row in table.findAll('tr')[1:]:
                    for header in row.findAll('th'):
                        if header.b is not None:
                            header_list.append(header.b.contents[0])    
                        else:    
                            header_list.append(header.contents[0])
                    cells = row.findAll('td')

                    try:
                        County = cells[0].a.contents[0]
                    except:
                        County = cells[0].contents[0]

                
                    try:
                        Trump = int(cells[Trump_index].b.contents[0].replace(',',''))
                    except:
                        Trump = int(cells[Trump_index].contents[0].replace(',',''))
                    try:
                        Clinton = int(cells[Clinton_index].b.contents[0].replace(',',''))
                    except:
                        Clinton = int(cells[Clinton_index].contents[0].replace(',',''))

                    if Johnson_index != -9999:
                        Johnson = int(cells[Johnson_index].contents[0].replace(',',''))
                    elif Johnson_index == -9999:
                        Johnson = 0
                    if Stein_index != -9999: 
                        Stein = int(cells[Stein_index].contents[0].replace(',',''))
                    elif Stein_index == -9999:
                        Stein = 0
                     
                    try:
                        if Other_index != -9999: 
                                Other = int(cells[Other_index].contents[0].replace(',',''))
                                
                        elif Other_index == -9999:
                                Other = int(cells[Total_index].contents[0].replace(',','')) - (Trump + Clinton + Johnson + Stein)
                    except:
                        Other = 0
                        
                    co_rows = [County, Clinton, Trump, Johnson, Stein, Other]
                    
                    state_results.append(co_rows)

                                    

                
        ### More than one sortable wikitable 
        else:
            table = soup.findAll('table', class_= 'wikitable sortable')
        
            for row in table[1].findAll('tr')[:1]:
                for header in row.findAll('th'):
                    if header.b is not None:
                        header_list.append(header.b.contents[0])    
                    else:    
                        header_list.append(header.contents[0])
                find_t_index = list(set(trump_headers).intersection(header_list))[0]
                find_c_index = list(set(clinton_headers).intersection(header_list))[0]
                find_j_index = list(set(johnson_headers).intersection(header_list))[0]
            Trump_index = header_list.index(find_t_index)
            Clinton_index = header_list.index(find_c_index)
            Johnson_index = header_list.index(find_j_index)
            if header_list.count("Stein#") == 1 or header_list.count("Stein") == 1:
                Stein_index = header_list.index(list(set(stein_headers).intersection(header_list))[0])
            elif header_list.count('Stein') == 0:
                Stein_index = -9999

            
            if header_list.count('Total') > 0:
                Total_index = header_list.index('Total')
            elif header_list.count('Total Votes') > 0:
                Total_index = header_list.index('Total Votes')
                
            for row in table[1].findAll('tr')[1:]:
                
                cells = row.findAll('td')
                
                County = cells[0].a.contents[0]
                Trump = int(cells[Trump_index].contents[0].replace(',',''))
                Clinton = int(cells[Clinton_index].contents[0].replace(',',''))
                Johnson = int(cells[Johnson_index].contents[0].replace(',',''))
                if Stein_index != -9999: 
                    Stein = int(cells[Stein_index].contents[0].replace(',',''))
                elif Stein_index == -9999:
                    Stein = 0
                try:
                    if Other_index != -9999: 
                        Other = int(cells[Stein_index].contents[0].replace(',',''))
                    elif Other_index == -9999:
                        Other = int(cells[Total_index].contents[0].replace(',','')) - (Trump + Clinton + Johnson + Stein)
                except:
                    pass
                co_rows = [County, Clinton, Trump, Johnson, Stein, Other]
                
                state_results.append(co_rows)
        print(state_results)

        with open(r'E:\GIS_DATA\GEO_242\Final_Project\ElectionResultAnalysis\%s.csv' % state[0].replace(' ',''), 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(state_results)
        f.close()

csv_file.close()

