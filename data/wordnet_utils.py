import os , glob
from nltk.corpus import wordnet as wn
import json
import pickle

def make_wn2_wn3():
    key_map = {}
    id_map = {}
    curr_path = os.getcwd() + "/"
    _rel_path = curr_path.split('/data/')[0]
    print(_rel_path)
    _path = _rel_path +'/data/wn2.1_3.0'
    print("PTH" , _path)
    mono_files = glob.glob(os.path.join(_path, '*.mono'))
    poly_files = glob.glob(os.path.join(_path, '*.poly'))

    for file_name in mono_files:
        with open(file_name) as fp:
            for each in fp.readlines():
                wn2_sense_key , wn2_synset_offs ,\
                    wn3_sense_key , wn3_synset_offs = each.strip().split(' ')

                ref_syn = wn.lemma_from_key(wn3_sense_key).synset()
                wn2_word = ref_syn.name().split('.')[0]
                wn2_pos = ref_syn.pos()
                key_map[wn2_sense_key] = [wn3_sense_key]
                id_map[(wn2_word , wn2_pos ,1)] = (wn3_sense_key , \
                                                        wn3_synset_offs , 1)


    for file_name in poly_files:
        with open(file_name) as fp:
            for each in fp.readlines():
                all_keys = each.strip().split(' ')
                wn2_sense_key , wn2_synset_offs , wn2_sense_number = \
                                                            all_keys[1].split(';')
                wn3_vals = [tuple(each.split(';')) \
                                for each in all_keys[2:]]
                key_vals = []
                id_vals = []
                for wn3_sense_key , wn3_synset_offs , wn3_sense_number in wn3_vals:
                    if wn3_sense_key:
                        id_vals.append((wn3_sense_key ,wn3_synset_offs ,\
                                                        wn3_sense_number))
                        key_vals.append(wn3_sense_key)

                if key_vals:
                    ref_syn = wn.lemma_from_key(key_vals[0]).synset()
                    wn2_word = ref_syn.name().split('.')[0]
                    wn2_pos = ref_syn.pos()
                    key_map[wn2_sense_key] = key_vals
                    id_map[(wn2_word , wn2_pos , wn2_sense_number)] = id_vals

    with open(_rel_path+"/data/wn3_id_map", "wb") as file_handle:
        pickle.dump(id_map, file_handle)

    with open(_rel_path+"/data/wn3_key_map" , "wb") as file_handle:
        pickle.dump(key_map , file_handle)
    return id_map , key_map
