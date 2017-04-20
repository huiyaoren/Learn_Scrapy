# coding: utf8

import json
import time
import os
import datetime

def get_data():

    ''' 从 json 文件读取信息 '''
    # BASE_DIR = os.path.dirname(__file__)
    # file_path = os.path.join(BASE_DIR, 'si_register.json')
    # print file_path
    # print os.getcwd()
    with open('si_register.json', 'r') as register:
        data = json.load(register)
        for d in data:
            print d['rgt_company_name'] , d['rgt_contact_phone'],d['rgt_company_size']

get_data()