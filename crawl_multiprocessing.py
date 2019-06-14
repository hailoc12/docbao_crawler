header = '''
#####################################################################################################################
#Program: docbao crawler
#Author: hailoc12
#Version: 1.0.0
#Date: 14/06/2019 
#Repository: http://github.com/hailoc12/docbao_crawler
#File: crawl.py
#Function: demo multiprocesseing crawling using firefox browser  
#####################################################################################################################
'''

# IMPORT LIB
from lib import *
import multiprocessing
import os
import time

def crawler_process(process_name, lock, browser_list, crawl_queue, crawled_data):
    # Function: work as an worker in multiprocessed crawling
    # Input:
    #   lock: to acquire and release shared data
    #   browser_list: a shared queue of browser to release when timeout
    #   crawl_queue: a shared queue of "crawl task"
    #   crawled_data: Queue that contain crawled data
    # Output:
    #   crawled_data: contain new crawled data

    print("Crawler %s has been started" % process_name)

    browser = BrowserWrapper()
    lock.acquire()
    browser_list.put(browser)
    lock.release()

    a = True
    while a:
    #try:
        while True:
            print("Crawler %s is running" % process_name)
            # get a web config from crawl_queue
            webconfig = None
            lock.acquire()
            if not crawl_queue.empty(): # have more job 
                webconfig = crawl_queue.get()
                lock.release()
                # crawl data
                print("Crawler %s is crawling page %s" % (process_name, webconfig.get_webname()))
                url = webconfig.get_crawl_url()
                html = utils.read_url_source(url, webconfig, browser)
                html_etree = etree.HTML(html)
                title = html_etree.xpath('//title/text()')[0]
                crawled_data.put({'webname': webconfig.get_webname(), 'title': title})
                
            else:
                lock.release()
                #print("Browser is")
                #print(browser)

                if browser is not None:
                    print("Quit browser in Crawler %s" % process_name)
                    browser.quit()
                print("Crawler %s is putting crawled data to main queues" % process_name)
                print("Crawler %s has finished" % process_name)
                return None
        a= False
    #except:
    #    print("There are some error in crawler %s" % process_name)
    #    if browser is not None:
    #        print("Quit browser in Crawler %s" % process_name)
    #        browser.quit()

# PROGRAM START HERE !

print(header)

### Change this !
crawl_urls = [{'webname':'Dân Trí', 'crawl_url':'http://dantri.com.vn'}, 
             {'webname':'Vietnamnet', 'crawl_url':'http://vietnamnet.vn'}, 
             {'webname':'Thanh Niên', 'crawl_url':'http://thanhnien.com.vn'}]
max_crawler = 3 # number of maximum Firefox browser can be used to crawl. Depend on server resources  

# Create Manager Proxy to host shared data for multiprocessed crawled
with multiprocessing.Manager() as manager:

    # share data between processes
    crawl_queue = manager.Queue() 
    crawled_data = manager.Queue()
    new_blacklists = manager.Queue()
    browser_list = manager.Queue() # keep all firefox browser to release when timeout
    lock = manager.Lock()
    timeout_flag = manager.Value('i', 0) # shared variable to inform processes if timeout happends

    # Init crawl queue
    number_of_job = 0
    for index in range(0, len(crawl_urls)):
        webconfig = WebConfig()
        webconfig.set_webname(crawl_urls[index]['webname'])
        webconfig.set_config('crawl_url', crawl_urls[index]['crawl_url'])
        webconfig.set_config('use_browser', True)
        # set another config here, see crawl_login_page.py for details
        #webconfig.set_config('browser_fast_load', True)
        #webconfig.set_config('browser_profile', 'test_profile')
        #webconfig.set_config('display_browser', True) #note: display_browser=True won't work in SSH mode
        
        crawl_queue.put(webconfig)

    # Start crawl process
    time.sleep(1)
    print("%s crawlers are set to be run in parallel" % str(max_crawler))
    crawler_processes = []
    time.sleep(1)
    print("Init %s crawlers" % str(max_crawler))

    start = time.time()

    for i in range(max_crawler):
        crawler = multiprocessing.Process(target=crawler_process, args=(str(i+1), lock, browser_list, crawl_queue, crawled_data))
        crawler_processes.append(crawler)
        crawler.start()
        time.sleep(1)
        print("Start crawler number %s (pid: %s)" % (str(i+1), crawler.pid))


        running = True
        running_crawler = ""
        count = 0

    while running:
        running = False
        count = 0
        for crawler in crawler_processes:
            count += 1
            if crawler.is_alive():
                running_crawler = running_crawler + " %s " % str(count)
                running = True
        print("Running crawler:")
        print(running_crawler)
        time.sleep(20)

    time.sleep(1)
    print("Finish crawling")
    time.sleep(1)

	# Print crawled data 
    print("Crawled data")

    while not crawled_data.empty():
        item = crawled_data.get()
        print("Page: %s" % item['webname'])
        print("Crawled data: %s" % item['title'])
        print()

print("FINISH")

