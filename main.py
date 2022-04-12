from email import header
from bs4 import BeautifulSoup
import json
import csv
import time
import urllib.request as urllib2
from numpy import product
import requests
import pandas as pd

 
#reading csv file
a=pd.read_csv("Amazon.csv")
x=a["Asin"]
y=a["country"]
s=[]
k=[]
url=[]
for a,b in zip(x,y):
     s.append(a)
     k.append(b)
for c,d in zip(s,k):
    url.append(f"https://www.amazon.{d}/dp/{c}")


# Function to extract Product Title
def get_title(soup):

    try:
        product_title = soup.find('span', class_= "a-size-large product-title-word-break")
        if product_title == None:
            product_title = soup.find('span', class_= "a-size-extra-large")
        if product_title != None:
            product_title = product_title.text
    
    except AttributeError:

        product_title=""
     
     
 
    return product_title

# Function to extract Product Img

def get_img(soup):
    try:
        productimg=soup.find("div",{"id":"imgTagWrapperId"})
        for item in productimg.find_all('img'):
            productimg=item['src']
    except AttributeError:
        productimg = ""

    return productimg

    
 
# Function to extract Product Price
def get_price(soup):
 
    try:
        price =  soup.find('span', {"class": "a-offscreen"})
        if price !=None:
            price=price.text

    except AttributeError:
        price = ""  
 
    return price

# Function to extract Product Description
 
def get_description(soup):
    product_details={}
    productDetailsTable = soup.find('table', class_= "a-normal a-spacing-micro")
    if(productDetailsTable != None):
        productDetailsRows= productDetailsTable.find_all('tr')
        if(productDetailsRows != None):
            for x in range(len(productDetailsRows)):
                tableRow = productDetailsRows[x]
                product_detail_key= tableRow.find_all('td')[0].find('span').text
                product_detail_value= tableRow.find_all('td')[1].find('span').text
                product_details[product_detail_key]= product_detail_value

    return product_details
if __name__ == '__main__':
 
    # Headers for request or user Agent
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    
    product_count = 0
    start_time = time.time()
    ID = 0
 
    # The webpage URL
    for pageURL in url:
        #checking conditions for 100 products
        if(product_count == 101):
            time_for_100_products = time.time()
            time_diff = time_for_100_products - start_time
            print("Time For 100 products: " + str(time_diff))
            start_time = time.time()
            product_count = 0
        
        #Agent url
        brouserAgentHeader = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
        #requesting url with urllib2
        req = urllib2.Request(pageURL, None, brouserAgentHeader)
        #printing id of product and url for scrapping
        print(f"ID is {ID} Scrapping link: {pageURL} \n")
        ID+=1
        
        
        try:
            req = urllib2.Request(pageURL, None, brouserAgentHeader) #requesting url with urllib2
            response = urllib2.urlopen(req) 
            content = response.read() #reading url means our content of page
            
            if response.getcode() == 200: #checking if getcode==200 then proceded
                product_description = {} #empty disc for savng product details
                soup = BeautifulSoup(content, "html.parser") #using beautifulsoup from bs4 with html.parser format 
                product_description["Product Name"] = get_title(soup) #appending details in product descrptions 
                product_description["Product Image"] = get_img(soup)
                product_description["Product Price"] = get_price(soup)
                product_description["Product Details"] = get_description(soup)
                product_description["Product Id"] = ID
                print()
                print()
                product_count += 1
                print(f"Saving product of ID {ID}") #saving message with product iD
                json_dump = json.dumps(product_description) #creating json data
                with open('amazon_products_data.json', 'a+') as f:  #opening json file
                    f.write(json_dump) #writing and updating product details in json file
                    f.write(",\n")
                    f.close()
                product_count += 1
                    
                
                
        except urllib2.URLError as e: #checking if urll is 404 or showing any error with error message 
            print(f"webpage not exist of ID {ID} error {e}")
            product_count += 1
            continue