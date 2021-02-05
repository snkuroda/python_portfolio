import arcpy, urllib2, os, csv, re
import pandas as pd
from bs4 import BeautifulSoup as BS

#   Access VA election page
url = r'http://results.elections.virginia.gov/vaelections/2016%20November%20General/Site/Locality/Index.html'
header = {'User-Agent': 'Mozilla/5.0'}
request = urllib2.Request(url, headers=header)
page = urllib2.urlopen(request)
headsoup = BS(page, "html.parser")
html_body = headsoup.body.findAll(id='tab-1')

# Parse html to get hyperlinks to each individual counties'/cities' election result page
base_url = r'http://results.elections.virginia.gov/vaelections/2016%20November%20General/Site/Locality/'
virginia_co_link = []
co_name = []

vir_csv = csv.writer(open("Virginia.csv", 'wb'))
for hmtl in html_body:
    for a in hmtl.findAll('a', href=True)[7:]:
        co_link = a['href'][2:]
        co_link_new = co_link.replace(' ', '%20')
        county = ' '.join(co_link.split(' ')[:-1])
        co_name.append(county)
        virginia_co_link.append(base_url + co_link_new)



# For each county parse table and get   
for co_url in virginia_co_link:
    print(co_url)
    county_name = ' '.join(((co_url.split('/')[-2]).split('%20')[:-1]))
    print(county_name)



    co_request = urllib2.Request(co_url, headers=header)
    co_page = urllib2.urlopen(co_request)
    soup = BS(co_page, "html.parser")
    result_table = soup.body.findAll('table')

    co_vote_list = []
    for result in result_table[:1]:
        votes = result.findAll('td', class_='votes')[:6]
        for vote in votes:
            co_vote_list.append(int(vote.contents[0].replace(',','')))
    
    if len(co_vote_list) == 6:
        Clinton = co_vote_list[0]
        Trump = co_vote_list[1]
        Johnson = co_vote_list[2]
        Stein = co_vote_list[3]
        Other = co_vote_list[4] + co_vote_list[5]
        
        vote_roll = [county_name, Clinton, Trump, Johnson, Stein, Other]
        print(vote_roll)

        vir_csv.writerow(vote_roll)

vir_csv.close
