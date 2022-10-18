import requests
from bs4 import BeautifulSoup
import json


class GarminScrapper():
    # Connect to given URL and create Beautiful Soup out of response. Then generate Json from data.
    def retreive_source_code(self, link,file_path):
        response = requests.request('GET', link)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.generate_json_data(file_path)
    # Find div with id garmin-app-bootstrap, convert it to string and slice it for dict conversion via saving and later
    # loading JSON file
    def generate_json_data(self,file_path):
        data_string = str(self.soup.find('div', {'id': 'garmin-app-bootstrap'}).string)
        start = data_string.index('{')
        end = data_string.index('};') + 1
        data_string = data_string[start:end]
        self.write_source_to_file(json.loads(data_string),file_path)

    # Write given string as json file so it will convert to dict easily later
    def write_source_to_file(self, data,file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


    # Function that obtains crucial data for description generator
    def obtain_description_data(self,file_path):
        # Create dictionary which will contain data for description generator
        product_description = {}
        # Open previously saved json file and convert it's data to source dictionary
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data_dict = dict(json.load(json_file))
        # Find product Part number
        product_description['PN'] = data_dict['sku']
        # Find product name
        product_description['NAME'] = data_dict['skus'][product_description['PN']]['productName']
        # Find product variation name
        product_description['VARNAME'] = data_dict['skus'][product_description['PN']]['productVariation']
        # From dictionary get content with given keys. After that convert it to Beautiful Soup object
        soup2 = BeautifulSoup(data_dict['skus'][product_description['PN']]['tabs']['overviewTab']['content'],features='lxml')
        #self.debug_write_file(soup2.prettify(), 'debug.txt')
        # Search for video banner
        try:
            product_description['VIDEO'] = soup2.find('pc-video-banner')['video-link']
        except:
            product_description['VIDEO'] = None
            print('Video not found')
        # Get first paragraph
        product_description['START'] = [soup2.find('pc-overview-intro')['title'],soup2.find('pc-overview-intro')['description']]
        # Get overview icons and description, first find pc-overview-intro section then get all feature cards to dict
        overview = soup2.find('pc-overview-intro')
        product_description['OVERVIEW'] = []
        for tag in overview.find_all('pc-feature-card'):
            product_description['OVERVIEW'].append([tag['image'],tag['description']])
        # Get product description - due to finding all feature cards, we need to slice table to get rid of overview cards
        description = soup2.find_all(['pc-life-style','pc-feature-card'])[len(product_description['OVERVIEW']):]
        product_description['DESCRIPTION'] = []
        for x in description:
            if x.name == 'pc-life-style':
                product_description['DESCRIPTION'].append([x.name,x['bg-image'],x['text']])
            elif x.name == 'pc-feature-card':
                try:
                    product_description['DESCRIPTION'].append([x.name,x['image'],x['title'],x['description']])
                except KeyError:
                    product_description['DESCRIPTION'].append([x.name, '',x['title'], x['description']])
                # Get disclaimer, key counter is numeration of disclaimers
        product_description['DISCLAIMER'] = []
        for element in soup2.find_all('pc-disclaimer-item'):
            product_description['DISCLAIMER'].append([element['counter'],element['content']])

        return product_description
    def obtain_table_data(self,file_path):
        scrapped_data = {}
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data_dict = dict(json.load(json_file))
        scrapped_data['PN'] = data_dict['sku']
        scrapped_data['TABLE'] = []
        soup = BeautifulSoup(data_dict['skus'][data_dict['sku']]['tabs']['specsTab']['content'],features='lxml')
        tags = soup.findAll(['th','td'])
        for x in tags:
            if x.name == 'th':
                scrapped_data['TABLE'].append(['row',x.text])
            elif x.name == 'td':
                try:
                    flag = x['colspan']
                except:
                    flag = 0
                if flag == '2':
                    scrapped_data['TABLE'].append(['paragraph', x.text])
                elif x.text != '':
                    scrapped_data['TABLE'][-1].append(x.text)
                else:
                    scrapped_data['TABLE'][-1].append('yes')
        return scrapped_data

    # Debug - Write file for research
    def debug_write_file(self,data,file_path):
        with open(f'{file_path}-debug.txt','w',encoding='utf-8') as debug_file:
            debug_file.write(data)