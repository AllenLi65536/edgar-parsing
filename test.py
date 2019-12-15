from nltk.corpus import wordnet as wn

nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

