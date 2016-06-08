'''
Created on May 3, 2016

@author: Abhay Gupta
'''
import urllib2, requests
from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, sys

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match

def has_classes(tag):
    '''
    Returns a list of all the matching classes of 'tag'
    '''
    hasClassesList = []
    possibleClassNames = ['tpjob_title', 'title', 'job_title', 'jobtitle']
    for possibleClass in possibleClassNames:
        if tag.has_attr(possibleClass):
            hasClassesList.append(possibleClass)
    return hasClassesList

def get_link_content(url, a_id):
    # use firefox to get page with javascript generated content
    with closing(Firefox()) as browser:
        browser.get(url)
        link = browser.find_element_by_id(a_id)
        link.click()
        # wait for the page to load
        WebDriverWait(browser, timeout=100).until(
            lambda x: x.find_element_by_id('lblreqname'))
        # store it to string variable
        page_source = browser.page_source
    return page_source

def get_job_details(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    data_job_name = soup.findAll('div', attrs={'id':'divjre'})
    for div in data_job_name:
        span = div.findAll('span')
        for a in span:
            print "Job Name =  ", str(a.text)

def get_company_profile(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    data = soup.findAll('span', attrs={'id':'lblCompanyprof'})
    for span in data:
        print "Company Profile =  ", str(span.text)

def get_job_description(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    data = soup.findAll('span', attrs={'id':'lblJD'})
    for span in data:
        print "Job Description =  ", str(span.text)

def get_job_title(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    data = soup.findAll('span', attrs={'id':'lbljobtitle'})
    for span in data:
        print "Job Title =  ", str(span.text)

def print_job_details(html_doc):
    count = 0
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.findAll('div',attrs={'id':'Openings1_updatepnl'})
    for div in data:
            links = div.findAll('a')
            for a in links:
                try:
                    count = count + 1
                    print a['id']
                    full_job_page = get_link_content(url, a['id'])
                    get_job_details(full_job_page)
                    get_company_profile(full_job_page)
                    get_job_description(full_job_page)
                    get_job_title(full_job_page)
                    
                except Exception as e:
                    print e
                    pass
    print "total jobs processed=", str(count)

def get_next_page(pagination_next_pg_id, url):
    with closing(Firefox()) as browser:
        browser.get(url)
        link = browser.find_element_by_id(pagination_next_pg_id)
        # wait for the page to load
        WebDriverWait(browser, timeout=100).until(
            lambda x: x.find_element_by_id(pagination_next_pg_id))
        link.click()
        # store it to string variable
    return browser

def get_next_page_link_content(browser, a_id):
    # use firefox to get page with javascript generated content
    #with browser:
    link = browser.find_element_by_id(a_id)
    try:
        #link = WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.ID, "a_id")))
        print 'link==', link.text
        print 'clicking...'
        link.click()
        #click = ActionChains(browser).move_to_element(link).click()
        #click = ActionChains(browser).move_to_element_with_offset(link, link.location.get('x'), link.location.get('y')).click()
        #click.perform()
        
        # wait for the page to load
        WebDriverWait(browser, timeout=5000).until(
                lambda x: x.find_element_by_id('lblreqname'))
    except Exception as e:
        print 'click exception= ', e
        print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
    # store it to string variable
    page_source = browser.page_source
    return page_source

def print_next_job_details(pagination_next_pg_id, url):
    browser_obj = get_next_page(pagination_next_pg_id, url)
    count = 0
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.findAll('div', attrs={'id':'Openings1_updatepnl'})
    for div in data:
            links = div.findAll('a')
            for a in links:
                try:
                    count = count + 1
                    full_job_page = get_next_page_link_content(browser_obj, a['id'])
                    get_job_details(full_job_page)
                    get_company_profile(full_job_page)
                    get_job_description(full_job_page)
                    get_job_title(full_job_page)
                except Exception as e:
                    print 'exception= ', e
                    print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)
    print "total jobs processed=", str(count)

if __name__ == '__main__':
    url = "http://www.jerryvarghese.com/Job-Search/ReqSearch.aspx?p=0&locID=121&loc=Saudi%20Arabia"
    response = requests.get(url)
    try:
        response.raise_for_status()
        html_doc = response.text
        #print_job_details(html_doc)
        for i in xrange(2,11):
            pagination_next_pg_id = 'lbtn' + str(i)
            #browser_obj = get_next_page(pagination_next_pg_id, url)
            print_next_job_details(pagination_next_pg_id, url)
    except Exception as e:
        print e
        print 'Line Number= ' + str(sys.exc_traceback.tb_lineno)