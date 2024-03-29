#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:         Zhanshuai Meng
#Created:        14 Oct 2015
#Version:        1.0
#Description:
#

import sys,os
import time
DEFAULT_SOURECE_DIR='./assignment2-data.txt'
DEFALUT_HASHTREE_DEGREE = 6
ITEM_NUM = 11
MINSUP = 0.144

#Node class of the hashtree
class Node:
    def __init__(self):
        self.leaf_node = False
        self.children_list = {}
        self.level = 0  #Level in the hash tree
        self.index = []

class Apriori:
    #Data file can be set manually
    def __init__(self,data_file=DEFAULT_SOURECE_DIR):
        #Each element corrosponds to a list
        self.transactions_list = []
        self.data_file = data_file
        self.candidate_set = []
        self.freq_counter = {} #dict
        self.k = 1 # frequent k-itemset
        self.freq_set = [] #list<list> [k] save the k+1 freq_item

    def set_candiate_set(self,candidate_set):
        self.candidate_set = candidate_set
        self.k = len(self.candidate_set[0])

    def read_from_file(self):
        with open(self.data_file,'r') as f:
            f.readline()
            for content_line in f:
                item_raw_list = content_line.split()
                item_list = [index for index,value in enumerate(item_raw_list) if int(value.strip()) == 1]
                #Record the index of value
                self.transactions_list.append(item_list) # Look like List<List>

    #Generate 1-freqset
    def get_freq1_itemset(self):
        item_counter = [0]*ITEM_NUM
        for item_list in self.transactions_list:
            for item in item_list:
                item_counter[int(item)] += 1
        single_freq_set = []
        threshold = MINSUP*len(self.transactions_list)*1.0
        for index, num in enumerate(item_counter):
            if num > threshold:
                set_list = []
                set_list.append(index)
                single_freq_set.append(set_list)
                self.freq_counter[tuple(set_list)]=num
        single_freq_set.sort()
        return single_freq_set

    def construct_hashtree(self,candidate_set,degree=DEFALUT_HASHTREE_DEGREE): # candidate set like List<list>
        root = Node()
        for index, sub_list in enumerate(candidate_set):
            parent_node =root
            for sub_index, item in enumerate(sub_list):
                hash_value = int(item)%degree
                if not hash_value in parent_node.children_list:
                    node = Node()
                    node.level = sub_index + 1 #Level increase from 1 by 1
                    parent_node.children_list[hash_value] = node  #save the canidate set index
                else:
                    pass
                if sub_index  == len(sub_list) - 1: # leaf node is flaged as true
                    parent_node.children_list[hash_value].leaf_node = True
                    sub_list.sort()
                    parent_node.children_list[hash_value].index.append(sub_list)
                else:
                    pass
                parent_node = parent_node.children_list[hash_value]
        return root


    def __explore_hashtree(self,transaction,root,prefix_list=[],degree=DEFALUT_HASHTREE_DEGREE): #recursive invokation
        level,length = len(prefix_list)+1,len(transaction) # level,length is set 0 at first
        gen_transaction = transaction[:]
        for item in  transaction[:len(transaction)-self.k+level]:
            current_child = root.children_list.get(int(item)%degree,[])
            if not current_child:
                #break
                continue
            gen_prefix_list = prefix_list[:]
            gen_transaction.remove(item) #Pop the 1st element always
            gen_prefix_list.append(item)
            if current_child.leaf_node:
                if gen_prefix_list in current_child.index:
                    gen_prefix_tuple = tuple(gen_prefix_list)
                    if self.freq_counter.get(gen_prefix_tuple,-1)==-1:#key 可以是list吗
                        self.freq_counter[gen_prefix_tuple] = 1
                    else:
                        self.freq_counter[gen_prefix_tuple] += 1
                gen_prefix_list.remove(item)
            else:
                if gen_transaction:
                    self.__explore_hashtree(gen_transaction,current_child,gen_prefix_list,degree)
        return



    def support_count(self,root):
        #invoke explore_hashtree
        for transaction in self.transactions_list:
            self.__explore_hashtree(transaction,root)
        threshold = MINSUP*len(self.transactions_list)*1.0
        length = len(self.freq_set[len(self.freq_set)-1][0])
        freq_set = [list(key) for key, value in self.freq_counter.items() if value >= threshold and len(key)>length]
        #freq_set
        freq_set.sort()
        self.freq_set.append(freq_set)

    def generate_candinate_set(self,freq_set):
        length = len(freq_set)
        itemset_length = len(freq_set[0])
        generate_candinate_set = []
        for index1 in range(0,length-1):
            continue_flag = False
            for index2 in range(index1+1,length):
                dif_set = list(set(freq_set[index1][:itemset_length-1]).difference(set(freq_set[index2][:itemset_length-1])))
                if (not dif_set) and (not itemset_length == 1): # dif_set is null
                    continue_flag = True
                    break
                union_set = list(set(freq_set[index1]).union(set(freq_set[index2])))
                if len(union_set) == itemset_length+1:
                    union_set.sort()
                    generate_candinate_set.append(union_set)
                else:
                    continue_flag = True
                    break
            if continue_flag:
                continue
            generate_candinate_set.sort()
        return generate_candinate_set

    def prune(self,candidate_set):
        temp_set = candidate_set
        k = len(candidate_set[0])
        for index, item_set in enumerate(candidate_set):
            candidate_flag = True
            remove_last_set = item_set[:]
            remove_last_set.pop(len(remove_last_set)-1)
            remove_last_set.pop(len(remove_last_set)-1) #zuihou 2 ge bu jiaru le, meibiyao
            for sub_index,item in enumerate(remove_last_set):
                sub_set = item_set[:]
                sub_set.pop(sub_index)
                sub_set.sort()
                if not sub_set in self.freq_set[k-2]:
                    candidate_flag = False
                    break
            if not candidate_flag:
                temp_set.remove(item_set)
                continue
        return temp_set

class Apriori_run:
    def __init__(self):
        self.alg = Apriori()
        self.alg.read_from_file()

    def run(self):
        self.alg.freq_set.insert(0,self.alg.get_freq1_itemset())
        k = 1
        while k<=len(self.alg.freq_set):
            prune_set = []
            candidate_set = self.alg.generate_candinate_set(self.alg.freq_set[k-1])
            if candidate_set:
                prune_set = self.alg.prune(candidate_set)
            if prune_set:
                self.alg.set_candiate_set(prune_set)
                root = self.alg.construct_hashtree(prune_set)
                self.alg.support_count(root)
                k += 1
            else:
                break

    def print_result(self):
        result = []
        for item_list in self.alg.freq_set:
            for freq_item in item_list:
                result.append(freq_item)
        result.sort()
        if os.path.isfile('result.txt'):
            os.remove('result.txt')
        with open('result.txt','a') as f:
            for item in result:
                final_item = [element+1 for element in item]
                freq = round(self.alg.freq_counter[tuple(item)]*1.0/len(self.alg.transactions_list),3)
                format_str = str(tuple(final_item)).lstrip('(').rstrip(')').rstrip(',')
                f.write(format_str.ljust(8)+'       '+str(freq)+'\n')


if __name__=='__main__':
    process = Apriori_run()
    process.run()
    process.print_result()
    print 'Conduct successfully'




































































