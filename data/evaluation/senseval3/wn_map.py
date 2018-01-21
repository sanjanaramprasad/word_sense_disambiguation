import os
import xml.etree.ElementTree as ET
import xmltodict
import io
import collections
from nltk.corpus import wordnet as wn
import re
import json
from xml.dom.minidom import parseString

def _preprocess(file_handle):
	all_lines = file_handle.readlines()
	all_lines = [re.sub("gloss=(.*)/>" , ' />',line) \
					for line in all_lines]
	contents = ''.join(all_lines)
	with open('dummy' , 'w') as f:
		f.write(contents)
	return contents


class WnMap():
	def __init__(self , input_file):
		self.input_file = input_file
		self._create_mapping()

	def _create_mapping(self):
		self.wn_map = {}
		fd = open(self.input_file ,"r")
		contents = _preprocess(fd)
		doc = xmltodict.parse(contents)
		_dicts = [each for k , v in doc['corpus'].items() \
						for each in v \
							if not type(each) is str ]
		count = 0
		for _dict in _dicts:
			senses = _dict['sense']
			for sense in senses:
				_id = sense['@id']
				if '@wn' in sense.keys():
					_wn_senses = sense['@wn'].split(';')
					self.wn_map[_id] = _wn_senses
				elif '%' in _id:
					self.wn_map[_id] = _id.split(';')



		with open('semeval3_map.json' ,'w') as fp:
			json.dump(self.wn_map , fp)

		return





WnMap('EnglishLS.dictionary.mapping.xml')
