import os
import xml.etree.ElementTree as ET
import xmltodict
import io
import collections
from nltk.corpus import wordnet as wn
import re
import json
import sys
from nltk.tokenize import sent_tokenize
_curr_path = os.getcwd()
_data_path = _curr_path.split('evaluation')[0]
sys.path.insert(0, _data_path)
from wordnet_map import *
global_list = []

class DataConverter:

    def __init__(self , input_file , output_file , map_file = None):
        self.input_file = input_file
        self.output_file = output_file
        self.map_file = map_file
        self.wn_map_obj = WordNetMap()

        if self.map_file:
            with open(self.map_file , 'r') as fp:
                self.senseval3_map = json.load(fp)
        self._make_data()
        return

    def _make_data(self):
        self.write_json = {}
        fd = io.open(self.input_file,"r",encoding='ISO-8859-1')
        contents = fd.read()
        doc = xmltodict.parse(contents)
        sentences = [each.split('</context>')[0] \
                        for each in contents.split('<context>')[1:]]
        count = 0
        for _dict in doc['corpus']['lexelt']:
            instances = _dict['instance']
            instances = instances if type(instances) is list else [instances]
            #print(instances)
            for each in instances:
                #print(each['@id'])
                #print('RAW TEXT' ,sentences[count])


                heads = each['context']['head']
                heads = heads if type(heads) is list else [heads]
                for head in heads:
                    if not type(head) is str:
                        head = each['context']['head']['#text']
                        sats = each['context']['sat']
                        if not type(sats) is list : sats = [sats]
                        sats_head = ' '.join([sat['#text'] for sat in sats])
                        print('HEAD' , head + ' '+sats_head)
                    #head = head if type is str else ' '.join([head['#text'],each['context']['sat']])
                    else:
                        print('HEAD' , head)

                shortlisted_texts = [text for text in sent_tokenize(sentences[count]) \
                                        if re.findall('<head(.*)</head|<sat(.*)</sat' , text) ]

                count+=1
                print('Preprocessed Text : ', ' '.join(shortlisted_texts))
                print('-'*20)


                '''answers = each['answer']
                if not type(answers) is list : answers = [each['answer']]
                if self.map_file:
                    _sense_keys = [_sense_key \
                                        for ans in answers\
                                            if ans['@senseid'] in self.senseval3_map.keys()
                                                for _sense_key in self.senseval3_map[ans['@senseid']]]

                else:
                    _sense_keys = [ans['@senseid'] \
                                        for ans in answers]


                for ans in answer:
                    if self.map_file :
                        ans['@senseid'] in self.senseval3_map.keys():
                        print(self.senseval3_map[ans['@senseid']])
                shortlisted_texts = [text for text in sent_tokenize(sentences[count]) \
            							if re.findall('<head(.*)</head|<sat(.*)</sat' , text) ]


                for each in _sense_keys:
                    each = each.strip()
                    return_value = self.wn_map_obj._get_key3_from_key2(each)
                    if not return_value:
                        try :
                            wn.lemma_from_key(each).synset()
                        except :
                            continue
                count+=1
                #print('Preprocessed Text : ', ' '.join(shortlisted_texts))
                #print('-'*20)

            for instance in _dict['instance']:
                try:
                    context = instance['context']
                    #print('-'*10)
                except :
                    print(_dict,  instance)
                    print('-'*10)'''
        print(count)
        return




'''##### For senseval 2 ########
senseval2_path = os.getcwd() + '/senseval2/english-lex-sample/test/'
senseval2_input = senseval2_path +'eng-lex-samp.evaluation.xml'
senseval2_output = 'senseval2.json'
DataConverter(senseval2_input , senseval2_output)'''

'''##### For senseval 3 ########
senseval3_path = os.getcwd() + '/senseval3/'
senseval3_input = senseval3_path +'EnglishLS.test'
senseval3_output = 'senseval3.json'
DataConverter(senseval3_input , senseval3_output , senseval3_path + '/semeval3_map.json')'''
