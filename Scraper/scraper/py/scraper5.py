# -*- coding: utf-8 -*- 
'''
Created on May 27, 2016

@author: abgupta
'''
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
import time, sys, traceback
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

class Scraper(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.url = 'http://www.jerryvarghese.com/Job-Search/ReqSearch.aspx?p=0&locID=121&loc=Saudi%20Arabia'
        #self.base_job_url = 'https://sjobs.brassring.com/TGWebHost/jobdetails.aspx?'
        self.browser = Firefox()
        self.first_page_search_opening_id = 'srchOpenLink'
        self.second_page_search_btn_id = 'ctl00_MainContent_submit2'
        self.next_link_id = 'yui-pg0-0-next-link'

    def page_links(self):
        job_link_id = 'Openings1_Rptr_FieldName_ct{}_lknReqTitle'
        for i in range(100, 115):
            link_id = job_link_id.format(str(i))
            link = self.browser.find_element_by_id(link_id)
            link.click()

    def main(self):
        try:
            self.browser.get(self.url)
            self.page_links()
            counter = 1
            

            
        except Exception as e:
            print 'exception= ', str(e)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)

if __name__ == '__main__':
    start_time = time.time()
    sys.stdout.flush()
    sys.stdout.write('\b')
    Scraper().main()
    sys.stdout.flush()
    sys.stdout.write('\b')
    end_time = time.time()
    print 'Processing Time = ',  str(end_time-start_time)