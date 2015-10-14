#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:         Zhanshuai Meng
#Created:        14 Oct 2015
#Version:        1.0
#Description:
#

import sys,os
import time
DEFAULT_SOURECE_DIR
class Apriori:
    def __init__(self,data_file=DEFAULT_SOURECE_DIR):
        #Each element corrosponds to a list
        self.transactions_list = []
        self.data_file = file

    def read_from_file(self):
        with open(self.data_file,'r') as f:
            for content_line in f:
                item_list = []
                item_raw_list = content_line.split()[1:]
                for index, value in emuerate(item_raw_list):
                    if int(value.strip())==1:
                        item_list.append(index)
                #Record the index of value
                self.transactions_list.append(item_list)







