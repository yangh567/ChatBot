import numpy as np
import nltk
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def doc2vec(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag


# sentence = ["hello", "how", "are", "you"]
# words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
# bog = bag_of_words(sentence, words)
# print(bog)
#
# a = "How long does shipping take?"
# print(a)
# a = tokenize(a)
# print(a)
#
# b = ["organize", "Organizes", "Organizing"]
# stemmed_words = [stem(w) for w in b]
# print(stemmed_words)


# # # CC coordinating conjunction
# # # CD cardinal digit
# # # DT determiner
# # # EX existential there (like: “there is” … think of it like “there exists”)
# # # FW foreign word
# # # IN preposition/subordinating conjunction
# # # JJ adjective ‘big’
# # # JJR adjective, comparative ‘bigger’
# # # JJS adjective, superlative ‘biggest’
# # # LS list marker 1)
# # # MD modal could, will
# # # NN noun, singular ‘desk’
# # # NNS noun plural ‘desks’
# # # NNP proper noun, singular ‘Harrison’
# # # NNPS proper noun, plural ‘Americans’
# # # PDT predeterminer ‘all the kids’
# # # POS possessive ending parent’s
# # # PRP personal pronoun I, he, she
# # # PRP$ possessive pronoun my, his, hers
# # # RB adverb very, silently,
# # # RBR adverb, comparative better
# # # RBS adverb, superlative best
# # # RP particle give up
# # # TO, to go ‘to’ the store.
# # # UH interjection, errrrrrrrm
# # # VB verb, base form take
# # # VBD verb, past tense took
# # # VBG verb, gerund/present participle taking
# # # VBN verb, past participle taken
# # # VBP verb, sing. present, non-3d take
# # # VBZ verb, 3rd person sing. present takes
# # # WDT wh-determiner which
# # # WP wh-pronoun who, what
# # # WP$ possessive wh-pronoun whose
# # # WRB wh-abverb where, when