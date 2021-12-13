'''
Takes input csv file
'''
import requests
import pandas as pd
from lxml import html
import datetime
import os
from  multiprocessing import Pool


OUTPUT_FOLDER = 'japan_output/'

def get_text(data):
    url = data['url']
    
    file_id = data['id']
    if not os.path.isdir(OUTPUT_FOLDER+data['filename']):
        os.mkdir(OUTPUT_FOLDER+data['filename'])
    file_name = OUTPUT_FOLDER+data['filename']+'/'+str(file_id)+'_' + datetime.datetime.now().strftime('%Y-%m-%d')
    print(file_name)
    if os.path.isfile(file_name + '_with_html.txt'):
        print("Already extracted!")
    else:
        print("Running the url",url)
        try:
            response = requests.get(url)
        except Exception as e:
            print(e)
            with open(OUTPUT_FOLDER+data['filename']+'/'+'_error_urls.txt','a', newline='\n') as errorfile:
                errorfile.write(str(file_id)+'\t'+ url + '\n')
            response = None
        if response:
            try:
            
                # with open(file_name+'_with_html.txt','w', encoding='utf-8') as f:
                #     f.write(response.text)
                page = html.fromstring(response.text)
                pages = ' '.join(page.xpath('//text()'))
                with open(file_name+'_texts.txt','w',encoding='utf-8') as p:
                    p.write(pages)
            except Exception as e:
                print(e)
                with open(OUTPUT_FOLDER+data['filename']+'/'+'_unicode_error_urls.txt','a', newline='\n') as errorfile:
                    errorfile.write(str(file_id)+'\t'+ url + '\t' )


if __name__ == '__main__':
    #INPUT_FILE = 'airbnb_JA_-_media_review_2021_12_10.xlsx - data.csv'
    INPUT_FOLDER = 'Japan'
    print("Reading input folder")
    list_dir = os.listdir(INPUT_FOLDER)
    print("Total files found are", len(list_dir))
    
    for file_ in list_dir:
        OUTPUT_FILE = 'output'
        excel_file = file_.split('_-_media')[0]
        df = pd.read_excel(INPUT_FOLDER +'/'+ file_)
        ids = df['ID'].to_list()
        urls = df['Link'].to_list()
        if len(ids) == len(urls):
            data_list = [{'id':ids[i], 'url':urls[i],'filename':excel_file} for i in range(len(urls))]
        else:
            with open('logs.txt','a') as logfile:
                logfile.write("Not equal for >>"+excel_file+'\n')
        with Pool(10) as p:
            print(p.map(get_text, data_list))
      
