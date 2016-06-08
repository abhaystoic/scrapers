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
        self.url = 'http://job-search.jobstreet.com.ph/philippines/job-opening.php?key=sykes+asia+inc&area=3&option=1&job-source=1%2C64&classified=1&job-posted=0&sort=1&order=0&pg={}&src=16&srcr=44'
        self.browser = webdriver.PhantomJS(executable_path='phantomjs.exe', 
                                           desired_capabilities=webdriver.DesiredCapabilities.HTMLUNITWITHJS
                                           )
        self.job_listing_id = 'job_listing_panel'
    
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
            
    def get_job_info(self, new_browser, job_url):
        try:
            new_browser.get(job_url)
            html = new_browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            f = open('jobs.txt','a')
            
            #Find designation
            data = soup.find('h1', attrs={'id' : 'position_title'})
            if data:
                #print data.text
                f.write(data.text.encode('utf-8').decode('ascii', 'ignore') + '\n')
            else:
                pass
                print 'Job not processed for url=', str(job_url)
            f.close()
            return 0
        except Exception as e:
            print 'exception= ', str(e)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)

    def get_jobs(self):
        try:
            #jobs_start_time = time.time()
            h = HTMLParser()
            html = h.unescape(self.browser.page_source).encode('utf-8').decode('ascii', 'ignore')
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.findAll('a', id=lambda x: x and x.startswith('position_title'))
            counter = 0
            for a in data:
                if a.has_attr('href'):
                    counter = counter + 1
                    #self.DrawSpinner(counter)
                    try:
                        return_code = self.get_job_info(self.browser, a['href'])
                        if return_code == 1:
                            #In case the error pages starts to come
                            #jobs_end_time = time.time()
                            #print 'All jobs scraping time =', str(jobs_end_time - jobs_start_time)
                            #print 'Total jobs processed=', counter
                            #print 'Job that may have got missed=', str(self.base_job_url + a['href'].split('?')[1]).split('&')[1].split('=')[1]
                            #return
                            pass
                            
                    except Exception:
                        continue
            print 'Total jobs processed=', counter
            #jobs_end_time = time.time()
            #print 'All jobs scraping time =', str(jobs_end_time - jobs_start_time)
        except Exception as e:
            print 'exception= ', str(e)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)

    def main(self, start_page, end_page):
        try:
            for page_num in xrange(start_page, end_page):
                self.browser.get(self.url.format(str(page_num)))
                self.get_jobs()
        except Exception as ex:
            print 'exception= ', str(ex)
            #print 'stacktrace= ', traceback.print_exc()
            print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
            
if __name__ == '__main__':
    start_time = time.time()
    sys.stdout.flush()
    sys.stdout.write('\b')
    start_page = int(sys.argv[1])
    end_page = int(sys.argv[2])
    Scraper().main(start_page, end_page)
    sys.stdout.flush()
    sys.stdout.write('\b')
    end_time = time.time()
    print 'Total Processing Time from', str(start_page), 'to', str(end_page), '=',  str(end_time-start_time)