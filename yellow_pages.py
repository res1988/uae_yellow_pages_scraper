import requests
from bs4 import BeautifulSoup
import os
import string
from time import sleep

root_url = 'https://www.yellowpages.ae/companies-by-alphabet/'
initial_url = root_url + 'a.html'

#alphabet_list = list(string.ascii_lowercase)

def get_bs_object(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

#get company links
def get_page_links(soup_object):
	# print (soup_object)
	for spn in soup_object.find_all('span', {'id': 'ContentPlaceHolder1_dlkeyword_detail'}):
		for link in spn.find_all('a'):
			print("link is:", link)
			data = [get_company_data(link['href'])]
			print (list(data))
			sleep(10)
			with open('company_data.txt', 'a') as f:
				f.write("|".join(list(data[0])) + '\n' )
	initial_url = soup_object.findAll('a', {'id':'ContentPlaceHolder1_DataListPaging_hlpaging_1'})[0]
	soup_object = get_bs_object(initial_url)
	return get_page_links(soup_object)

#get company data
def get_company_data(company_url):
	company = get_bs_object(company_url)
	try:
		get_coordinates = company.find_all('div', {'id':'ContentPlaceHolder1_divDirection'})[0].find('a')['href'].replace(' ', '')
	except:
		get_coordinates="N/A"
	get_name = company.findAll('h1')[0].find('span').text
	get_category = company.findAll('div', {'id': 'ContentPlaceHolder1_divCategory'})[0].find('a')['title']
	return get_coordinates, get_name, get_category

soup_object = get_bs_object(initial_url)
get_page_links(soup_object)