from lib.utils import *
import pytz
import yaml
from datetime import timedelta

# class represents config to crawl a specific website
class WebConfig:
    def __init__(self, web={"webname":{}}):
        self._web = web # dict of dict {"webname":{"url":...,date_tag:[...], date_class:[...]}

    def get_config(self, key, default):
        if key not in self._web[self.get_webname()]:
            self.set_config(key, default)
            return default
        else:
            return self._web[self.get_webname()][key]

    def set_webname(self, webname):
        old_name = self.get_webname()
        self._web={webname: self._web[old_name]}

    def get_webname(self):
        return next(iter(self._web))

    def get_weburl(self):
        return self._web[self.get_webname()]['web_url']

    def get_crawl_url(self):
        return self._web[self.get_webname()]['crawl_url']

    def get_url_pattern_re(self):
        return self._web[self.get_webname()]['url_pattern_re']

    def get_crawl_type(self):
        return self.get_config('crawl_type', 'xpath')

    def get_topics_xpath(self):
        return self.get_config('topics_xpath', '//a')
    def get_topic_type(self):
        return self.get_config('topic_type', "text")
    def get_date_xpath(self):
        return self.get_config('date_xpath', '')

    def get_date_re(self):
        result = self._web[self.get_webname()]['date_re']
        if(not isinstance(result, list)): #compatible with older config version
            return [result]
        else:
            return result

    def get_date_pattern(self):
        result = self._web[self.get_webname()]['date_pattern']
        if(not isinstance(result, list)):
            return [result]
        else:
            return result

    def get_date_place(self):
        return self.get_config('date_place', 'detail_page')
    def get_limit_repeat_topic(self):
        return self.get_config('limit_repeat_topic', False)

    def get_timezone(self):
        '''
        output: pytz.timezone class 
        '''
        try:
            result = pytz.timezone(self.get_config('timezone', 'UTC'))
        except:
            print("Wrong timezone format. Please provide one in tz database (google it)")
            print("Choose UTC by default")
            result = pytz.timezone("UTC")
        return result

    def get_language(self):
        return self._web[self.get_webname()]['language']
    def get_id_type(self):
        return self.get_config('id_type', 'href')

    def get_skip_crawl_publish_date(self):
        return self._web[self.get_webname()]['get_publish_date_as_crawl_date']

    def get_extract_xpath(self):
        return self.get_config('extract_xpath', ["*/text()"])
    def get_use_index_number(self):
        return self.get_config('use_index_number', False)

    def get_topic_from_link(self):
       return self.get_config('get_topic_from_link', True)
    def get_output_html(self):
        return self._web[self.get_webname()]['output_html']
    def get_use_browser(self):
        return self._web[self.get_webname()]['use_browser']
    def get_display_browser(self):
        return self.get_config("display_browser", False)
    def get_browser_timeout(self):
        return self.get_config("browser_timeout", 60)
    def get_browser_fast_load(self):
        return self.get_config('browser_fast_load', True)
    def get_browser_profile(self):
        return self.get_config('browser_profile', None)
    def get_contain_filter(self):
        return self.get_config("contain", "")
    def get_maximum_url(self):
        '''
        function: get max number of link that will be crawl in this website in one call
        '''
        return self.get_config("maximum_url", 10)

    def get_last_run(self):
        last_run_string = self.get_config('last_run', get_utc_now_date() - timedelta(days=7))
        if isinstance(last_run_string, str):
            naive_last_run = datetime.strptime(last_run_string, "%d/%m/%Y %H:%M")
            aware_last_run = self.get_timezone().localize(naive_last_run)
            return aware_last_run
        else:
            last_run = last_run_string
            self.set_last_run(last_run)
            return last_run

    def get_minimum_topic_length(self):
        return self.get_config('minimum_topic_length', 4)

    def set_last_run(self, date=None):
        if date is None:
            date = get_utc_now_date()
        self.set_config('last_run', utils.get_date_string(date, "%d/%m/%Y %H:%M", self.get_timezone()))

    def get_minimum_duration_between_crawls(self):
        return self.get_config('minimum_duration_between_crawls', 5)

    def set_minimum_duration_between_crawls(self, value):
        self.set_config('get_minimum_duration_between_crawls', value)

    def set_config(self, key, value):
        self._web[self.get_webname()][key] = value

