# coding:utf-8
# ����������ķ���
from selenium import webdriver
import requests
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DoubanSpider(object):
    '''
    ��������
    '''
    def __init__(self, user_name, password, headless = False):
        '''
        ��ʼ��
        :param user_name: �����¼�û���
        :param password: �����¼�û�����
        :param headless: �Ƿ���ʾwebdriver���������
        :return: None
        '''
        self.user_name = user_name
        self.password = password
        self.headless = headless

        # ��¼
        self.login()
        
    def login(self):
        '''
        ��¼�����־û�cookie
        :return: None
        '''
        # �����¼ҳ��URL
        login_url = 'https://www.douban.com/accounts/login'

        # ��ȡchrome������
        opt = webdriver.ChromeOptions()
        # �����е�ʱ�򲻵������������
        if self.headless:
            opt.set_headless()

        # ��ȡdriver����
        self.driver = webdriver.Chrome(chrome_options = opt)
        # �򿪵�¼ҳ��
        self.driver.get(login_url)

        print '[login] opened login page...'

        # ������������û��������룬�������¼��ť
        self.driver.find_element_by_name('form_email').send_keys(self.user_name)
        self.driver.find_element_by_name('form_password').send_keys(self.password)
        # ��ε�¼��Ҫ������֤�룬�����һ���ֹ�������֤���ʱ��
        time.sleep(6)
        self.driver.find_element_by_class_name('btn-submit').submit()
        print '[login] submited...'
        # �ȴ�2����
        time.sleep(2)

        # ����һ��requests session����
        self.session = requests.Session()
        # ��driver�л�ȡcookie�б���һ���б��б��ÿ��Ԫ�ض���һ���ֵ䣩
        cookies = self.driver.get_cookies()
        # ��cookies���õ�session��
        for cookie in cookies:
            self.session.cookies.set(cookie['name'],cookie['value'])

    def get_page_source(self, url):
        '''
        ��ȡ����������е�ҳ��HTML����
        :param url: ��ҳ����
        :return: ��ҳҳ��HTML����
        '''
        self.driver.get(url)
        page_source = self.driver.page_source
        print '[get_page_source] page_source head 100 char = {}'.format(page_source[:100])
        return page_source
    
    def get(self, url, params = None):
        '''
        ��һ��url����get���󣬷���response����
        :param url: ��ҳ����
        :param params: URL�����ֵ�
        :return: ����������ȡ��response����
        '''
        resp = self.session.get(url, params = params)

        if resp:
            print '[get] status_code = {0}'.format(resp.status_code)
            resp.encoding = 'utf-8'
            # �������Ҫ��ÿ�η�������󣬶�����session��cookie����ֹcookie����
            if resp.cookies.get_dict():
                self.session.update(resp.cookies)
                print '[get] updated cookies, new cookies = {0}'.format(resp.cookies.get_dict())
            return resp
        else:
            print '[get] response is None'
            return None
    def get_html(self,url, params = None):
        '''
        ��ȡһ��url��Ӧ��ҳ���HTML����
        :param url: ��ҳ����
        :param params: URL�����ֵ�
        :return: ��ҳ��HTML����
        '''
        resp = self.get(url)
        if resp:
            return resp.text
        else:
            return ''

class DoubanDiscussionSpider(DoubanSpider):
    '''
    ����С�����ۻ�������
    '''
    def __init__(self, user_name, password, group_name, headless = False):
        '''
        ��ʼ��
        :param user_name: �����¼�û���
        :param password: �����¼�û�����
        :param group_name: ����С������
        :param headless: �Ƿ���ʾwebdriver���������
        :return: None
        '''
        super(DoubanDiscussionSpider,self).__init__(user_name, password, headless)
        self.group_name = group_name

        # ����С�������б�URLģ��
        self.url = 'https://www.douban.com/group/{group_name}/discussion'.format(group_name = self.group_name)
        print '[__init__] url = {0}'.format(self.url)

    def get_discussion_list(self, start=0, limit=100):
        '''
        ��ȡ�����б�
        '''

def sample():
    '''
    ����
    '''
    user_name = sys.argv[1]
    password = sys.argv[2]
    group_name = 'nanshanzufang'
    spider = DoubanDiscussionSpider(user_name, password, group_name)

    # ��Ҫ��¼���ܿ�����ҳ��URL
    page_url = 'https://www.douban.com/accounts/'
    # ��ȡ��ҳ����
    html = spider.get_page_source(page_url)
    # ����ҳ���ݴ����ļ�
    with open('html.txt','w+') as  fout:
        fout.write(html)    

if __name__ == '__main__':
    sample()
    print 'end'
