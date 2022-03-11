# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import unidecode

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2003


    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if (spider.name=='hhru'):
            ready_salary = self.process_salary_hhru(item['salary'])
            item['source'] = 'hh.ru'
        else:
            if (spider.name=='sjru'):
                ready_salary = self.process_salary_sjru(item['salary'])
                item['source'] = 'superjob.ru'

        item['min_salary'] = ready_salary['min_salary']
        item['max_salary'] = ready_salary['max_salary']
        item['currency'] = ready_salary['currency']
        del item['salary']

        collection.insert_one(item)
        return item

    def process_salary_sjru(self, salary):
        ready_salary={}
        if (salary[0]=='По договорённости') or (salary==[]):
            ready_salary['min_salary']=None
            ready_salary['max_salary'] = None
            ready_salary['currency'] = None
        else:
            if (salary[0]=='от') :
                    salary_currency = unidecode.unidecode(salary[2])
                    salary_currency = salary_currency.split(' ')
                    ready_salary['currency'] = salary_currency[-1]
                    ready_salary['min_salary'] = int(salary_currency[0] + salary_currency[1])
                    ready_salary['max_salary'] = None
            else:
                if (salary[0]=='до') :
                        ready_salary['min_salary'] = None
                        salary_currency = unidecode.unidecode(salary[2])
                        salary_currency = salary_currency.split(' ')
                        ready_salary['currency'] = salary_currency[-1]
                        ready_salary['max_salary'] = int(salary_currency[0]+salary_currency[1])
                else:
                        ready_salary['min_salary'] = int(unidecode.unidecode(salary[0]).replace(' ', ''))
                        ready_salary['max_salary'] = int(unidecode.unidecode(salary[1]).replace(' ', ''))
                        ready_salary['currency'] = salary[3]
        return ready_salary


    def process_salary_hhru(self, salary):
        ready_salary={}
        if (salary[0]=='з/п не указана') or (salary==[]):
            ready_salary['min_salary']=None
            ready_salary['max_salary'] = None
            ready_salary['currency'] = None
        else:
            if (salary[0]=='от ') and (salary[2]==' до '):
                ready_salary['min_salary'] = int(unidecode.unidecode(salary[1]).replace(' ', ''))
                ready_salary['max_salary'] = int(unidecode.unidecode(salary[3]).replace(' ', ''))
                ready_salary['currency'] = salary[5]
            else:
                if (salary[0]=='от ') :
                    ready_salary['min_salary'] = int(unidecode.unidecode(salary[1]).replace(' ', ''))
                    ready_salary['max_salary'] = None
                    ready_salary['currency'] = salary[3]
                else:
                    if (salary[0]=='до ') :
                        ready_salary['min_salary'] = None
                        ready_salary['max_salary'] = int(unidecode.unidecode(salary[1]).replace(' ', ''))
                        ready_salary['currency'] = salary[3]


        return ready_salary