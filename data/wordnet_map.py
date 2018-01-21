import wordnet_utils as wu
import os.path
import pickle

curr_path = os.getcwd() + "/"
_rel_path = curr_path.split('/data/')[0]
id_file = _rel_path + '/data/wn3_id_map'
key_file = _rel_path + '/data/wn3_key_map'

class WordNetMap:

    def __init__(self):
        if not (os.path.isfile(id_file) and os.path.isfile(key_file)):
                    wu.make_wn2_wn3()
        with open(id_file , 'rb') as fp:
            self.id_map = pickle.load(fp)
        with open(key_file , 'rb') as fp:
            self.key_map = pickle.load(fp)

        return

    def _get_key3_from_key2(self , lemma_key):
        lemma_key = lemma_key.strip()
        if lemma_key in self.key_map.keys():
            return self.key_map[lemma_key]
        return []
