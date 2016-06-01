# -*- coding: utf-8 -*- 
'''
Created on May 27, 2016

@author: abgupta
'''
from selenium import webdriver
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
        self.browser = webdriver.PhantomJS(executable_path='phantomjs.exe', 
                                           desired_capabilities=webdriver.DesiredCapabilities.HTMLUNITWITHJS,
                                           service_args=['--load-images=no']
                                           )
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
        try:
            #Click search button 
            link = self.browser.find_element_by_id(self.second_page_search_btn_id)
            link.click()
            # wait for the page to load
            WebDriverWait(self.browser, timeout=100).until(
                lambda x: x.find_element_by_class_name('t_full'))
        except Exception as e:
            print 'exception= ', str(e)
            print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)

    def click_next_button(self):
        try:
            #Click NEXT
            link = self.browser.find_element_by_id(self.next_link_id)
            link.click()
            # wait for the page to load
            WebDriverWait(self.browser, timeout=100).until(
                lambda x: x.find_element_by_class_name('t_full'))
        except Exception as e:
            print 'exception= ', str(e)
            print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
                
    def get_page_source(self):
        page_source = self.browser.page_source.decode('utf8')
#         f = open('myhtml.html','a')
#         f.write(page_source)
#         f.close()
        return page_source
    
    def get_job_info(self, new_browser, job_url):
        try:
            new_browser.get(job_url)
            html = new_browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            find_error = soup.find('div', attrs={'id' : 'errorid'})
            if find_error:
                return 1
            #Find designation
            data = soup.find('span', attrs={'id' : 'Designation'})
            if data:
                #print data.text
                f = open('jobs.txt','a')
                f.write(data.text + ' :: ')
                f.close()  
            else:
                pass
            
            #Find Qualifications
            data_ql = soup.find('span', attrs={'id' : 'Qualification'})
            if data_ql:
                #print data_ql.text
                f = open('jobs.txt','a')
                f.write(data_ql.text + ' :: ')
                f.close()
            else:
                pass
                
            #Find Removal Date
            data_rd = soup.find('span', attrs={'id' : 'Removal Date'})
            if data_rd:
                #print data_ql.text
                f = open('jobs.txt','a')
                f.write(data_rd.text + '\n')
                f.close()
            else:
                pass
            return 0
        except Exception as e:
            print 'exception= ', str(e)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
            return 1
    def get_jobs(self):
        try:
            h = HTMLParser()
            html = h.unescape(self.browser.page_source).encode('utf-8').decode('ascii', 'ignore')
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.findAll('a', id=lambda x: x and x.startswith('popup'))
            counter = 0
            for a in data:
                if a.has_attr('href'):
                    counter = counter + 1
                    #self.DrawSpinner(counter)
                    try:
                        return_code = self.get_job_info(self.browser, self.base_job_url + a['href'].split('?')[1])
                        if return_code == 1:
                            #In case the error pages starts to come
                            return
                    except Exception:
                        continue
        except Exception as e:
            print 'exception= ', str(e)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
    
    def click_pages(self, actual_page_number):
            for i in range(10, actual_page_number + 1, 4):
                try:
                    self.browser.find_elements_by_css_selector('a[page="{}"]'.format(str(actual_page_number)))[0].click()
                    print 'Page number ff', str(actual_page_number), 'clicked'
                    # wait for the page to load
                    WebDriverWait(self.browser, timeout=100).until(
                        lambda x: x.find_element_by_class_name('t_full'))
                    return
                except Exception as e:
                    try:
                        #If the actual page number is not on the screen
                        print 'page', str(actual_page_number), 'not found. i==', str(i), str(e)
                        self.browser.find_elements_by_css_selector('a[page="{}"]'.format(str(i + 4)))[0].click()
                        # wait for the page to load
                        WebDriverWait(self.browser, timeout=100).until(
                            lambda x: x.find_element_by_class_name('yui-pg-pages'))
                    except:
                        continue

    def main(self):
        self.first_page(self.url)
        self.click_search_button()
        self.get_jobs()
        try:
            for i in xrange(2, int(5274/50) + 1):
                try:
                    self.first_page(self.url)
                    self.click_search_button()
                except Exception as e:
                    print 'exception= ', str(e)
                    #print 'stacktrace= ', traceback.print_exc()
                    print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
                    print 'Starting iteration again...'
                    #Ignore this iteration and start this iteration again
                    i = i - 1
                    continue
                if i > 10:
                    #Click page 10
                    self.browser.find_elements_by_css_selector('a[page="{}"]'.format('10'))[0].click()
                    self.click_pages(i)
                elif i != 1:
                    self.browser.find_elements_by_css_selector('a[page="{}"]'.format(str(i)))[0].click()
                    print 'Page number', str(i), 'clicked'
                self.get_jobs() 
#                 for _ in range(1, i+1):
#                     self.click_next_button()
        except Exception as ex:
            print 'exception= ', str(ex)
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