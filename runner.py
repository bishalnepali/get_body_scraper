'''
Takes input csv file
'''
import requests
import pandas as pd
from lxml import html
import datetime
import os
import threading


def get_text(data):
    url = data['url']
    
    file_id = data['id']
    file_name = 'output/'+str(file_id)+'_' + datetime.datetime.now().strftime('%Y-%m-%d')
    if os.path.isfile(file_name + '_with_html.txt'):
        print("Already extracted!")
    else:
        print("Running the url",url)
        try:
            response = requests.get(url)
        except Exception as e:
            print(e)
            with open('error_urls.txt','a', newline='\n') as errorfile:
                errorfile.write(str(file_id)+'\t'+ url + '\n')
            response = None
        if response:
            try:
            
                with open(file_name+'_with_html.txt','w', encoding='utf-8') as f:
                    f.write(response.text)
                page = html.fromstring(response.text)
                pages = ' '.join(page.xpath('//text()'))
                with open(file_name+'_without_html.txt','w',encoding='utf-8') as p:
                    p.write(pages)
            except Exception as e:
                with open('unicode_error_urls.txt','a', newline='\n') as errorfile:
                    errorfile.write(str(file_id)+'\t'+ url + '\t' )


def main(data):
    get_text(data)
if __name__ == '__main__':
    #INPUT_FILE = 'airbnb_JA_-_media_review_2021_12_10.xlsx - data.csv'
    INPUT_FOLDER = 'INPUT'
    print("Reading input folder")
    list_dir = os.listdir(INPUT_FOLDER)
    print("Total files found are", len(list_dir))
    for file_ in list_dir:
        OUTPUT_FILE = 'output'
        df = pd.read_csv(INPUT_FOLDER +'/'+ file_)
        ids = df['ID'].to_list()
        urls = df['Link'].to_list()
        if len(ids) == len(urls):
            data_list = [{'id':ids[i], 'url':urls[i]} for i in range(len(urls))]
        else:
            breakpoint()
        for data in data_list:
            main(data)
      
