from bs4 import BeautifulSoup
import requests
import sqlite3
import hashlib

conn = sqlite3.connect('yp.db')
c = conn.cursor()

# Create yellow pages table
# c.execute('''CREATE TABLE IF NOT EXISTS y_pages_category_lookup 
#         (category text)''')
# c.execute('''DROP TABLE IF EXISTS y_pages''')
# c.execute('''CREATE TABLE IF NOT EXISTS y_pages
#              (id text primary key, category text, name text, name_url text, location text, emirate text, page_url)''')
# conn.commit()s

def get_url_content(main_url):
    r = requests.get(main_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# logging data from a new page
def get_main_url_data(soup,main_url):
    for advert in soup.find_all("section", {"class": "left"}):
        id =  abs(hash(advert.find_all('a')[0]['href'].strip()))
        category = advert.find_all('a')[-1].text
        name = advert.find_all('a')[0].text
        name_url = advert.find_all('a')[0]['href'].strip()
        emirate = advert.find_all('div', {'class':'addr'})[0].find_all('div')[1].find_all('span')[-1].text
        location = '' 
        c.execute("INSERT or REPLACE INTO y_pages VALUES (?,?,?,?,?,?,?)", 
            (id
                , category
                , name 
                , name_url
                , location
                , emirate
                , main_url
                ))
        conn.commit()
    main_url = get_next_page(soup)
    if main_url != None:
        soup = get_url_content(main_url)
        return (get_main_url_data(soup, main_url))

#scroll through pages - get next page
def get_next_page(soup):
    try:
        next_url = soup.find_all('div', {"class": "sponsored_listings_numbring_right"})[0].find_all('a')[-1].text.replace('>>','').strip()
        if soup.find_all('div', {"class": "sponsored_listings_numbring_right"})[0] \
            .find_all('a')[-1].text.replace('>>','').strip() == 'Next':
            next_page = soup.find_all('div', {"class":"sponsored_listings_numbring_right"})[0].find_all('a')[-1]['href']
            return next_page
    except IndexError:
        return None

# get the details from one web page
emirate = 'uae'
category = ['shopping-centres','theme-parks','water-parks','hotels']

for cat in category:
    print("getting category %s"%(cat))
    main_url = 'https://www.yellowpages.ae/c/advs/{0}/{1}.html'.format(emirate, cat)
    soup = get_url_content(main_url)
    get_main_url_data(soup, main_url)

#update location
#update_yp_locations()

def update_yp_locations():
    update_list =c.execute('SELECT id,name_url FROM y_pages where location = ""').fetchall()
    for dat in update_list:
        company = get_url_content(dat[1])
        try:
            get_coordinates = company.find_all('div', {'id':'ContentPlaceHolder1_divDirection'})[0].find('a')['href'].replace(' ', '')
        except:
            get_coordinates="N/A"
        c.execute('''UPDATE y_pages
                SET location = ?
                WHERE id = ? ''', (get_coordinates, dat[0]))
        conn.commit()

update_yp_locations()    
print("process complete")


#to do
# get location details for each place
# scroll through pages to get the other places
# build category lookup
# build company name lookup
