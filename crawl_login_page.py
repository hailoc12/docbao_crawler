header='''
#####################################################################################################################
#Program: docbao crawler
#Author: hailoc12
#Version: 1.0.0
#Date: 14/06/2019 
#Repository: http://github.com/hailoc12/docbao_crawler
#File: crawl_login_page.py
#Function: demo crawl single login needed page (like Facebook) using firefox browser  
#####################################################################################################################
'''

from lib import *

print(header)

### CHANGE THIS !
url = 'https://www.facebook.com/?ref=tn_tnmn' # crawl page. 

# set crawl configuration 
webconfig = WebConfig() # object contains crawl configuration for a specific website 
webconfig.set_config('use_browser', True) # Use Firefox browser to crawl or not 
webconfig.set_config('browser_fast_load', True) # use adblock extensions, disable css...to load page faster  
webconfig.set_config('display_browser', False) # note: display_browser=True won't work if program is run through SSH 

### NOTICE THIS !
# note: you must create firefox profile test_profile first by running setup_browser.sh then use it to login Facebook by your own accout  
webconfig.set_config('browser_profile', 'test_profile')

browser = BrowserWrapper() # wrapper to get back reference to Firefox browser created in read_url_source function  

# main call here !!!
html = read_url_source(url, webconfig, browser)

# extract data 
if html is not None: #crawl ok
    html_tree = etree.HTML(html) #use lxml to parse HTML to element tree
    post_etree = html_tree.xpath("//div[@data-testid='post_message']")[0] # extract tag that contain first post on your homepage 
    post_string = utils.remove_html(utils.get_tagstring_from_etree(post_etree)) # remove html to get post content
    print("---------------------------------------------")
    print("The first post on your Facebook homepage is: ")
    print(post_string)
    
# quit browser to avoid memory leak: IMPORTANT !
browser.quit()
