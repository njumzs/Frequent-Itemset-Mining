#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:         Zhanshuai Meng
#Created:        14 Oct 2015
#Version:        1.0
#Description:
#

import sys,os
import time
DEFAULT_SOURECE_DIR=''
DEFALUT_HASHTREE_DEGREE = 6
ITEM_NUM = 11
MINSUP = 0.144

class Node:
    def __init__(self):
        self.leaf_node = False
        self.children_list = []
        self.level = 0  #Level in the hash tree
        self.index = []



class Apriori:
    def __init__(self,data_file=DEFAULT_SOURECE_DIR):
        #Each element corrosponds to a list
        self.transactions_list = []
        self.data_file = file
        self.candidate_set = []
        self.freq_counter = {} #dict
        self.k = 1 # frequent k-itemset
        self.freq_set = [] #list<list> [k] save the k+1 freq_item

    def set_candiate_set(self,candidate_set):
        self.candidate_set = candidate_set
        self.k = len(self.candidate_set[0])

    def read_from_file(self):
        with open(self.data_file,'r') as f:
            for content_line in f:
                item_raw_list = content_line.split()[1:]
                item_list = [index for index,value in emuerate(item_raw_list) if int(value.strip()) == 1]
                #Record the index of value
                self.transactions_list.append(item_list) # Look like List<List>

    def get_freq1_itemset(self):
        item_counter = [0]*ITEM_NUM
        for item_list in self.transactions_list:
            for item in item_list:
                item_counter[int(item)] += 1
        single_freq_set = []
        for index, num in enumerate(item_counter):
            if num*1.0/len(self.transactions_list) > MINSUP:
                single_freq_set.append(index)
        return single_freq_set.sort()

    def construct_hashtree(self,candidate_set,degree=DEFALUT_HASHTREE_DEGREE): # candidate set like List<list>
        root = Node()
        for index, sub_list in enumerate(candidate_set):
            parent_node =root
            for sub_index, item in enumerate(sub_list):
                hash_value = int(item)%degree
                children = parent_node.children_list[hash_value]
                if not children:
                    node = Node()
                    node.level = sub_index +1 #Level increase from 1 by 1
                    node.index.append(index)
                    parent_node.children_list[hash_value] = node  #save the canidate set index
                else:
                    parent_node_children_list[hash_value].index.append(index)
                if sub_index == len(sub_list)-1: # leaf node is flaged as true
                    parent_node_children_list[hash_value].leaf_node = True
                else:
                    pass
        return root


    def __explore_hashtree(self,transaction,root,prefix_list=[],degree=DEFALUT_HASHTREE_DEGREE): #recursive invokation
        level,length = len(prefix_list),len(transaction) # level,length is set 0 at first
        gen_transaction = transaction
        for item in  transaction[:len(transaction)-self.k+level+1]:
            current_child = root.children_list[int(item)%degree]
            if not current_child:
                break
            gen_prefix_list = prefix_list
            gen_transaction.pop(0) #Pop the 1st element always
            gen_prefix_list.append(item)
            if current_child.leaf_node:
                if self.freq_counter.get(gen_prefix_list,-1)==-1:#key 可以是list吗
                    self.freq_counter[gen_prefix_list]=0
                else:
                    self.freq_counter[gen_prefix_list] += 1
                return
            self.__explore_hashtree(gen_transaction,current_child,gen_prefix_list,degree)
        return



    def support_counting(self):
        #invoke explore_hashtree
        #########################
        #########################
        #########################
        #########################
        #########################
        #########################
        #########################
        #########################

    def generate_candinate_set(self,candinate_set):
        length = len(candidate_set)
        itemset_length = len(candidate_set[0])
        generate_candinate_set = []
        for index1 in range(0,length-1):
            continue_flag = False
            for index2 in range(index1+1,length):
                dif_set = list(set(candinate_set[index1][:itemset_length-1]).difference(set(candidate_set[index2][:itemset_length-1])))
                if not dif_set: # dif_set is null
                    continue_flag = True
                    break
                union_set = list(set(candidate_set[index1]).union(set(candidate_set[index2])))

               if len(union_set) == itemset_length+1:
                   generate_candinate_set.append(union_set.sort())
                else:
                    continue_flag = True
                    break
            if continue_flag:
                continue
        return generate_candinate_set

    def prune(self,candidate_set):
        temp_set = candidate_set
        k = len(candidate_set[0])
        for index, item_set in enumerate(candidate_set):
            candidate_flag = True
            for sub_index,item in enumerate(item_set):
                single_list = []
                single_list.append(item)
                sub_set = list(set(item_set).difference(set(single_list))).sort()
                if not sub_set in self.freq_set[k-1]:
                    candidate_flag = False
                    break
            if not candidate_flag:
                temp_set.remove(item_set)
                continue









































































