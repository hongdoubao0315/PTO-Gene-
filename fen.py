# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 19:32:49 2020

@author: Asus
"""

# -*- coding:utf-8 -*-
#! usr/bin/env python3
"""
Created on 11/03/2020 下午8:26 
@Author: xinzhi yao
"""
import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from collections import defaultdict
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk
import os

def read_pto(pto_file):
    """
    读取PTO文件 存为字典
    key: pto term id
    value: name and synonym
    :param pto_file: PTO 文件
    :return: 字典
    """
    opt_dic = defaultdict(list)  #存储PTOid，name，sym（近义词）。一个位置存放三个地方
    count_term = 0  #PTO数量
    count_word = 0  #包括名字和其近义词的数量
    with open(file=pto_file,mode='r',encoding="utf-8") as f:
        for line in f:
            l = line.strip()
            if l.startswith('id'): #id开头的话，存储
                count_term += 1
                id = l.split()[1]  #去除PTOid
            if l.startswith('name'):
                # 读取名字
                count_word += 1
                name = ' '.join(l.split(' ')[1:])
                if '(' in name:
                    name = name[:name.find('(') - 1 ]  #取出name，去除（）
                opt_dic[id].append(name)
            if l.startswith('synonym'):
                # 正则匹配读取同义名
                count_word += 1
                pattern = re.compile('"(.*)"')
                synonym = pattern.findall(l)[ 0 ]   #讲列表转为字符串

                pattern_ba = re.compile(r'[(].*?[)]')  #取出括号内容
                backets = pattern_ba.findall(l)
                if synonym.startswith('('):  #讲除第一个之后的括号都删除
                    for ba in backets[ 1: ]:
                        synonym = synonym.replace(ba, '')
                        synonym = synonym.strip(' ')
                else:  #如果开头没有括号，则所有括号都删除
                    for ba in backets:
                        synonym = synonym.replace(ba, '')
                        synonym = synonym.strip(' ')
                opt_dic[id].append(synonym)
    print('一共 {0} terms, 包含 {1} 个名字及同义名.'.format(count_term, count_word))
    return opt_dic

def abs_read(abstract_file: str):
    # 读取摘要 因为文件不大就全部存进内存了
    title_abstract_list = []
    count_abs = 0  #统计读到第几篇摘要
    with open(file=abstract_file,mode='r',encoding="utf-8") as f:
        line = f.readline()
        for line in f:
            l = line.strip().split('\t')  #按照制表符分隔
            try:
                pmid = l[0]
                title = l[1]  #Title
                abs = l[5]   #Abstract
                title_abstract_list.append((pmid,title, abs))
                count_abs += 1
            except:   #处理异常
                print(l)
                continue
    print('共 {0} 篇摘要.'.format(count_abs))
    return title_abstract_list

# 获取单词的词性
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

#词性分析后进行词性还原
#输入文件：word_list 单词列表
#输出文件：list_words_lemmatizer单词词形还原列表,list_sents_lemmatizer句子词形还原
def tag_lemmatizer(word_list):
    tagged_words = pos_tag(word_list)
    wnl = WordNetLemmatizer()
    list_words_lemmatizer = []
    for tag in tagged_words:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        list_words_lemmatizer.append(wnl.lemmatize(tag[0], pos=wordnet_pos)) 
    sents_lemmatizer=(" ".join(list_words_lemmatizer))   #分句词性还原
    return list_words_lemmatizer,sents_lemmatizer

#对PTO进行词形还原
def PTO_lem(pto_dic):
    pto_lem_dic = defaultdict(list) 
    for term,name_list in pto_dic.items():
        for name in name_list:
            name_lem,names_lem=tag_lemmatizer(word_tokenize(name))  #PTO词形还原
            pto_lem_dic[term].append(names_lem)
    return pto_lem_dic

def save_result(ta_list: list, pto_dic: dict, pto_lem_dic: dict, out_file: str):
    # 硬匹配搜索
    print('PTO search running.')
    wf = open(out_file, 'w' , encoding="utf-8")
    wf.write('PTO\tsentence\tpmid\tterm\n')   #输出文件标题行
    count = 0#记录载入的摘要
    count_result = 0 
    for ta in ta_list:  #摘要文件
        count += 1
        if count % 600 == 0:
            print('{0}/{1} abstracts process done.'.format(count, len(ta_list)))
        pmid = ta[0]
        abs = ta[2]  #abstract
        sent_list = [i for i in sent_tokenize(abs)]  #对摘要进行句子的分句
        for sent in sent_list:
            # 迭代每个句子
            word_list = word_tokenize(sent)
            # 分词
            words_lem,sent_lem=tag_lemmatizer(word_list)
            #摘要词性还原
            for term, name_list in pto_lem_dic.items():  
                #{'num1': 'Tom', 'num2': 'Lucy'}
                #dict_items([('num1', 'Tom'), ('num2', 'Lucy')])
                for name in name_list:
                    # 迭代PTO名字和同义名
                    if len(name.split(' ')) > 1:  #用所有name和sym匹配
                        # 如果PTO名字是一个词组 转换为小写直接在句子里匹配
                        names=word_tokenize(name)
                        a=0
                        word = [i.lower() for i in words_lem]  #摘要词转小写
                        for i in names:
                            a+=1
                            if i not in stop_words and i.lower() in word:  
                            #去除停用词
                            #if i.lower() in words_lem:  #不去停用词
                                if a==len(names):
                                    wf.write('{0}\t{1}\t{2}\t{3}\n'. \
                                             format(term, sent, pmid, '|'.join(pto_dic[term])))
                                    count_result += 1
                            else:
                                break
                    else:   #这里未变化大小写
                        if name in words_lem:  #不转小写，避免去除An这类关键词
                            # 如果PTO名字是单个单词 在分词列表中匹配
                            # 这样做是基于经验的做法 会更加准确
                                wf.write('{0}\t{1}\t{2}\t{3}\n'. \
                                     format(term, sent, pmid, '|'.join(pto_dic[term])))
                                count_result += 1
    print('共找到 {0} 个句子包含pto条目.'.format(count_result))
    wf.close()

def main(pto_file, abs_file, out_file):
    pto_dic = read_pto(pto_file)   #读取PTO文件
    # print(pto_dic)
    ta_list = abs_read(abs_file)  #读取摘要文件
    pto_lem_dic=PTO_lem(pto_dic)   #获取PTO词形还原
    save_result(ta_list, pto_dic, pto_lem_dic,out_file)  #寻找PTO

if __name__ == '__main__':
    pto_file = 'C:/Users/Asus/Desktop/TO_basic.obo'
    abs_file = 'C:/Users/Asus/Desktop/reference_PMID.match.table.txt'
    out_file = 'C:/Users/Asus/Desktop/result_fen.txt'
    with open('C:/Users/Asus/Desktop/stop_words.txt','r',encoding='utf-8') as fr:
        stop_words=fr.read().split('\n') #将停用词读取到列表里

    if not os.path.exists('../data'):  #如果不存在data，则创建data目录
        os.mkdir('../data')

    """
    类似的还可以提供其他规则提高匹配的准确性,
    例如nltk包里的词性分析 词性还原 提取词根词缀等方式匹配,
    提高召回率
    """
    print('-'*50)
    print('running.')
    main(pto_file, abs_file, out_file)
    print('Done.')
    print('-'*50)
