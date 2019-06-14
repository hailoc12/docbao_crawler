import urllib.request
from bs4 import BeautifulSoup
import re
import codecs
from datetime import datetime
import os
from  lib.browser_crawl import *
import time
import psutil
import pytz
from selenium import webdriver
from lxml import etree

_firefox_browser = None

# UTILITY FUNCTION
def get_independent_os_path(path_list):
    path = ""
    for item in path_list:
        path = os.path.join(path, item)
    return path

def get_utc_now_date():
    return pytz.utc.localize(datetime.utcnow())

def get_date_string(date, date_format, timezone):

    '''
    input
    -----
    timezone: tzinfo subclass

    output
    -----
    string

    '''
    return date.astimezone(timezone).strftime(date_format)

def get_max_crawler_can_be_run():
    # get max crawler that system can support (base on free ram)
    ram_for_each_crawler = 350000000
    safe_margin = 0.5 # free 45% for safe
    mem = psutil.virtual_memory()
    swap_free = psutil.swap_memory().free
    mem_free = (mem.free + swap_free) * safe_margin
    return int(mem_free  / ram_for_each_crawler)

def read_url_source(url, webconfig,_firefox_browser=BrowserWrapper()):
    '''
    function: use browser to get url pagesource
    --------

    output:
    -------
    None if can't read url  
    HTML source string if ok, _firefox_browser refer to the browser that is used
    '''

    hdr = {
        'user-agent': 'mozilla/5.0 (x11; linux x86_64) applewebkit/537.11 (khtml, like gecko) chrome/23.0.1271.64 safari/537.11',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'accept-charset': 'iso-8859-1,utf-8;q=0.7,*;q=0.3',
        'accept-encoding': 'none',
        'accept-language': 'en-us,en;q=0.8',
        'connection': 'keep-alive'}

    use_browser = webconfig.get_use_browser()
    _display_browser = webconfig.get_display_browser()
    _fast_load= webconfig.get_browser_fast_load()
    timeout= webconfig.get_browser_timeout()
    profile_name = webconfig.get_browser_profile()

    a=True
    result = False
    browser = None
    while a:
    #try:
        html_source = None
        if use_browser == False:
            req = urllib.request.Request(
                url,
                data=None,
                headers=hdr)
            f=None
            try:
                f = urllib.request.urlopen(req, timeout=30)
            except:
                f=None
                print("request timeout")
            if f is None:
                result = False
            else:
                result = True
                html_source = f.read().decode('utf-8')
        else:
            print("use browser to open %s" % url)
            if _firefox_browser.get_browser() is not None:
                browser = _firefox_browser.get_browser()
            else:
                print("create new instance of firefox browser")

                browser = BrowserCrawler(display_browser=_display_browser, fast_load=_fast_load, profile_name= profile_name)
                _firefox_browser.set_browser(browser)

            print("load page: %s" % url)
            result = browser.load_page(url, timeout, 5)
            print("browser load page result %s" % str(result))
            if result == True:
                try:
                    time.sleep(3) # there must be little delay between browser.load_page and get_page_html
                    html_source = browser.get_page_html() #somehow this command occasionally have errors
                except:
                    print("get page html error")
                    result = False
        a = False
        if result == True:
            return html_source
        else:
            return None
    #except:
    #    print("can't open " + url)
    #    return none

def quit_browser():
    global _firefox_browser

    if _firefox_browser is not None:
        print("found an running instance of firefox. close it")
        print(_firefox_browser)
        _firefox_browser.quit()

# html function
def remove_html(html_string):
    return BeautifulSoup(html_string,features="lxml").get_text()

def get_tagstring_from_etree(html_tree):
    tagstring = str(etree.tostring(html_tree, encoding='utf-8'), encoding='utf-8')
    return tagstring

# firefox functions

def get_firefox_profile(profile_name):
    '''
    function: return profile if exists, else create new
    input
    -----
    profile_name (str): profile in name
    '''
    profile_path = get_independent_os_path(['profiles',profile_name])
    
    if os.path.isdir(profile_path):
        return webdriver.FirefoxProfile(profile_path)
    else:
        print("profile %s doesn't exist yet") 
        print("i will create profile path at %s" % profile_path)
        print("then you need to create %s profile with setup_browser.py")
        print("you default profile in this session") 
        os.mkdir(profile_path)
        return None


