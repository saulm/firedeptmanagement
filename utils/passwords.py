import itertools
import random
import string
import os
import hashlib
from base64 import encodestring as encode
initial_consonants = (set(string.ascii_lowercase) - set('aeiou')
                      # remove those easily confused with others
                      - set('qxc')
                      # add some crunchy clusters
                      | set(['bl', 'br', 'cl', 'cr', 'dr', 'fl',
                             'fr', 'gl', 'gr', 'pl', 'pr', 'sk',
                             'sl', 'sm', 'sn', 'sp', 'st', 'str',
                             'sw', 'tr'])
                      )

final_consonants = (set(string.ascii_lowercase) - set('aeiou')
                    # confusable
                    - set('qxcsj')
                    # crunchy clusters
                    | set(['ct', 'ft', 'mp', 'nd', 'ng', 'nk', 'nt',
                           'pt', 'sk', 'sp', 'ss', 'st'])
                    )

vowels = 'aeiou' # we'll keep this simple

# each syllable is consonant-vowel-consonant "pronounceable"
syllables = map(''.join, itertools.product(initial_consonants, 
                                           vowels, 
                                           final_consonants))

# you could throw in number combinations, maybe capitalized versions... 

def gibberish(wordcount, wordlist=syllables):
    return random.sample(wordlist, wordcount)
    
def get_pronounceable_password(wordcount=1, digitcount=3):
    numbermax = 10 ** digitcount
    password = ''.join(gibberish(wordcount))
    if digitcount >= 1:
        password += str(int(random.random()*numbermax))
    return password

def makeSecret(password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    return "{SSHA}" + encode(h.digest() + salt)

