import os
import xml.etree.ElementTree as ET
import xmltodict
import io
import collections
from nltk.corpus import wordnet as wn
import re
import json
from nltk.tokenize import sent_tokenize


def _get_word_indices(_words , _text , _syns ):
	texts = []
	shortlisted_texts = [text for text in sent_tokenize(_text) \
							if re.findall('head>(.*)</head' , text) ]

	default_sense = _syns[0]
	default_word = _words[0]
	default_text = shortlisted_texts[0]

	len_words = len(_words)
	len_text = len(shortlisted_texts)
	len_syns = len(_syns)

	all_pairs = { k : {'words':{}} for k in shortlisted_texts}

	for i in range(max([len_words , len_text , len_syns])):
		sent = shortlisted_texts[i] if i < len_text else default_text
		word = _words[i] if i < len_words else default_word
		syn = _syns[i] if i< len_syns else default_sense
		all_pairs[sent] 






class DataConverter:

	def __init__(self , input_file , output_file):
		self.input_file = input_file
		self.output_file = output_file
		with open('/Users/srampras/artificial_data_generator/rnn_wsd/senseval_3/senseval3_map.json') as file_handle:
			self.map_senseval3 = json.load(file_handle)
		self._lex_sample()
		#self._write_file()



	def _lex_sample(self):
		#train_dir = str(os.getcwd()) + '/english-lex-sample/train/'
		#train_file = 'eng-lex-sample.training.xml'
		self.write_json = {}
		fd = io.open(self.input_file,"r",encoding='ISO-8859-1')
		#fd = open(self.input_file , "r")
		contents = fd.read()
		doc = xmltodict.parse(contents)

		sentences = [each.split('</context>')[0] for each in contents.split('<context>')[1:]]
		count = 0
		#print(sentences)
		for _dict in doc['corpus']['lexelt']:
			#print(_dict)
			for instance in _dict['instance']:
				#print('T',instance['context']['#text'])
				#print(instance['@id'])
				#print('-'*5)
				_word = instance['context']['head']
				if type(_word) is not list:
					_word = [_word] if type(_word) is str else [_word['#text']]

				sensekeys = instance['answer']
				if type(sensekeys) is list:
					labels = [each['@senseid'] for each in sensekeys]
				else:
					labels = [sensekeys['@senseid']]

				new_labels = []
				for each in labels:
					if 'senseval_3' in self.output_file:
						if each in self.map_senseval3.keys():
							each = self.map_senseval3[each] 
					try:
						new_labels.append(wn.lemma_from_key(each).synset().name())
					except:
						continue


				_word_indices = _get_word_indices(_word , sentences[count] , list(set(new_labels)))
				count += 1

				'''#print('S',sentences[count] )

				_sent = ' '.join([each for each in sentences[count].split('\n') \
											if list(set(_word).intersection(set(word_tokenize(each))))])
				_sent = re.sub('<[^>]*>' , ' ', _sent)
				#print(_dict['@item'])
				#print('TEXT' , instance['context']['#text']
				
				sensekeys = instance['answer']
				if type(sensekeys) is list:
					labels = [each['@senseid'] for each in sensekeys]
				else:
					labels = [sensekeys['@senseid']]
				new_labels = []

				if len(_word) > 1:
					print(_sent , _word , labels)
					print('='*10)
				count += 1


				for each in labels:
					if 'senseval_3' in self.output_file:
						if each in self.map_senseval3.keys():
							each = self.map_senseval3[each] 
					try:
						new_labels.append(wn.lemma_from_key(each).synset().name())
					except:
						continue

				#print(new_labels)
				count += 1
				
				if new_labels:
					word_dict = {'words' : {}}
					#for each in new_labels:
					#{'text': 'court', 'lemma': 'court', 'pos': 'NOUN', 'sense': 'court.n.02', 'break_level': 'NO_BREAK'}
					append_dict= {'text' : _word , 'sense' : new_labels[0]}


					self.write_json['s'+str(count)] = {'sentence' : _sent , 'words': {_word : append_dict}}
				#print('-'*10)
				count += 1
		print(self.write_json)'''

		return

	def _write_file(self):
		with open(self.output_file, 'w') as outfile:
			json.dump(self.write_json, outfile)

#DataConverter('/Users/srampras/artificial_data_generator/rnn_wsd/semeval_2/english-lex-sample/train/eng-lex-sample.training.xml')
DataConverter('/Users/srampras/artificial_data_generator/rnn_wsd/senseval_3/EnglishLS.train' , 'senseval_3.json')