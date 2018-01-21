from nltk.corpus import wordnet as wn


def _print_wn(_word):
    count = 1
    for each in wn.synsets(_word):
        print('KEY', each.lemmas()[0].key())
        print('OFFS' , str(each.offset()).zfill(8))
        print('DEF' ,each.definition())
        print('POS' , each.pos())
        print('SENSE NUM' , count)
        print('SYNS' ,each.lemma_names())
        print('HYPO' , each.hyponyms())
        print('EX' , each.examples())
        count += 1
        print('='*10)


_print_wn('fine')
