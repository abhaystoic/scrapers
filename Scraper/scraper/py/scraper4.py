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
        self.url = 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25667&siteid=5417'
        self.base_job_url = 'https://sjobs.brassring.com/TGWebHost/jobdetails.aspx?'
        self.browser = Firefox()
        self.first_page_search_opening_id = 'srchOpenLink'
        self.second_page_search_btn_id = 'ctl00_MainContent_submit2'
        self.next_link_id = 'yui-pg0-0-next-link'
    
    #Spinner
    def DrawSpinner(self, counter):
        if counter % 4 == 0:
            sys.stdout.write("/")
        elif counter % 4 == 1:
            sys.stdout.write("-")
        elif counter % 4 == 2:
            sys.stdout.write("\\")
        elif counter % 4 == 3:
            sys.stdout.write("|")
        sys.stdout.flush()
        sys.stdout.write('\b')
            
    def first_page(self, url):
        try:
            self.browser.get(url)
            #link = self.browser.find_element_by_link_text('Search openings')
            link = self.browser.find_element_by_id(self.first_page_search_opening_id)
            link.click()
            # wait for the page to load
            WebDriverWait(self.browser, timeout=100).until(
                lambda x: x.find_element_by_id(self.second_page_search_btn_id))
        except Exception as e:
            print 'exception= ', str(e)
            print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
    
    def click_search_button(self):
        #Click search button 
        link = self.browser.find_element_by_id(self.second_page_search_btn_id)
        link.click()
        # wait for the page to load
        WebDriverWait(self.browser, timeout=100).until(
            lambda x: x.find_element_by_class_name('t_full'))
    
    def click_next_button(self):
        #Click NEXT
        link = self.browser.find_element_by_id(self.next_link_id)
        link.click()
        # wait for the page to load
        WebDriverWait(self.browser, timeout=100).until(
            lambda x: x.find_element_by_class_name('t_full'))
    
    def get_page_source(self):
        page_source = self.browser.page_source.decode('utf8')
        f = open('myhtml.html','a')
        f.write(page_source)
        f.close()
        return page_source
    
    def get_job_info(self, new_browser, job_url):
        try:
            new_browser.get(job_url)
            html = new_browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            #Find designation
            data = soup.find('span', attrs={'id' : 'Designation'})
            if data:
                #print data.text
                f = open('descriptions.txt','a')
                f.write(data.text + '\n')
                f.close()  
            else:
                pass
            
            #Find Qualifications
            data_ql = soup.find('span', attrs={'id' : 'Qualification'})
            if data_ql:
                #print data_ql.text
                f = open('descriptions.txt','a')
                f.write(data_ql.text + '\n')
                f.close()
            else:
                pass
        except Exception as e:
            print 'exception= ', str(e)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)

    def get_jobs(self): 
        try:
            h = HTMLParser()
            html = h.unescape(self.browser.page_source).encode('utf-8').decode('ascii', 'ignore')
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.findAll('a', id=lambda x: x and x.startswith('popup'))
            #print data
            counter = 0
            for a in data:
                if a.has_attr('href'):
                    counter = counter + 1
                    self.DrawSpinner(counter)
                    try:
                        self.get_job_info(self.browser, self.base_job_url + a['href'].split('?')[1])
                    except Exception:
                        continue
            print counter
        except Exception as e:
            print 'exception= ', str(e)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)

    def main(self):
        self.first_page(self.url)
        self.click_search_button()
        self.get_jobs()
        self.click_next_button()
        try:
            for _ in (1, int(5309/50) + 1):
                self.get_jobs()
                self.click_next_button()
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