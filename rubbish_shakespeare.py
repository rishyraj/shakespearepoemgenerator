import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import cmudict
import sys
import random as r
import pickle
import numpy as np

def getTotal(tuples):
    total = 0
    for t in tuples:
        total+=t[1]
    return total

def format(text):
    return_text = ""
    i_conv = {'i':'I',"i'm":"I'm","i'll":"I'll"}
    ct = True
    for word in text:
        if (return_text[len(return_text)-1:] == "!" or return_text[len(return_text)-1:] == "?" or return_text[len(return_text)-1:] == "."):
            ct=True
            return_text+=" "
        if (ct):
            word = word.title()
            if ("'" in word):
                tempWord = word
                p1 = tempWord[:tempWord.index("'")]
                p2 = tempWord[tempWord.index("'"):]
                p2 = p2.lower()
                word = p1+p2
            return_text+=word
            ct=False
            continue
        if (return_text==""or word == ',' or word=='.' or word==':' or word=='?' or word=="!" or word==";" or word=="'" or word=="’"):
            return_text+=word
        elif (word=='i' or word=='I\'m' or word=="i'll"):
            return_text+=" "+i_conv[word]
        else:
            return_text+=" "+word
    return return_text

def transitionState(elements,probabilities):
    choice = ["("]
    ctr = 0
    while (choice[0]=="(" or choice[0]==")" or choice[0]=="[" or choice[0]=="]"):
        choice = np.random.choice(elements,1,p=probabilities)
        ctr+=1
        if (ctr==20):
            choice[0] = "."
    if choice[0]==':': return ","
    return choice[0]
def syllables(word):
    #referred from stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

def processAndSaveToPickle():
    with open("text/shakespeare.txt",encoding='utf-8') as f:
        text_original=f.read()
        f.close()
    text_original = text_original.lower()
    tknzr = TweetTokenizer()
    tokenized_text = tknzr.tokenize(text_original)
    word_after_dict = {}
    for i in range(len(tokenized_text)):
        if (i==len(tokenized_text)-1):
            break
        keyList = set(word_after_dict.keys())
        w1 = tokenized_text[i]
        w2 = tokenized_text[i+1]
        if (w1.isdigit() or w2.isdigit()):
            continue
        if (w1 not in keyList):
            word_after_dict[w1]=[]
        if (len(word_after_dict[w1]) == 0):
            word_after_dict[w1].append((w2,1))
        else:
            getTuples = word_after_dict[w1]
            word_found = False
            index_found = -1
            for tup in getTuples:
                index_found+=1
                word_in_tup = tup[0]
                if (word_in_tup==w2):
                    word_found = True
                    break
            if (word_found):
                num = word_after_dict[w1][index_found][1]
                num+=1
                newTup = (word_after_dict[w1][index_found][0],num)
                word_after_dict[w1][index_found]=newTup
            else:
                word_after_dict[w1].append((w2,1))
    file = open('shakespeare.pickle','wb')
    pickle.dump(word_after_dict,file,protocol=pickle.HIGHEST_PROTOCOL)
    file.close()
def loadPickle(filename):
    file = open(filename,'rb')
    word_after_dict = pickle.load(file)
    file.close()
    return word_after_dict
def generateRubbishShakespeare(word_after_dict):
    word_list = word_after_dict.keys()
    # seed_words = np.random.choice(list(word_list),10)
    seed_words = (np.random.choice(list(word_list),1))[0]
    # output_text_poem = []
    # for seeds in list(seed_words):
    #     l = [seeds]
    #     output_text_poem.append(l)
    # rubbish_shakespeare = ""
    rubbish_shakespeare=""
    non_letters = "()[];:,.!?'"
    sd_wd = ""
    for i in range(10):
        rubbish_shakespeare+="\n"
        ctr = -1
        if (i==0):
            output_text = [seed_words.title()]
        else:
            output_text = [sd_wd.title()]
        syllable_count = syllables(output_text[len(output_text)-1])
        chosen_word = ""
        hit = False
        while (True):
            ctr+=1
            w1 = chosen_word
            if (ctr==0):
                w1 = output_text[len(output_text)-1].lower()
            get_words = word_after_dict[w1]
            words_elements = []
            words_probs = []
            total = getTotal(get_words)
            for words in get_words:
                words_elements.append(words[0])
                words_probs.append(words[1]/total)
            chosen_word = transitionState(words_elements,words_probs)
            if (chosen_word not in non_letters):
                try:
                    syllable_count+=len(syllables(chosen_word))
                except TypeError:
                    syllable_count+=syllables(chosen_word)
            else:
                syllable_count+=0
            if (syllable_count>=10 and hit):
                if (chosen_word=="." or chosen_word=="\'" or chosen_word=="‘" or chosen_word=="." or chosen_word=="?" or chosen_word=="!" or chosen_word=="," or chosen_word==";"):
                    output_text.append(chosen_word)
                    continue
                sd_wd = chosen_word
                break
            if (chosen_word!="." or chosen_word!="'" or chosen_word!="‘"):
                output_text.append(chosen_word)
            else:
                continue
            if(syllable_count>=10):
                hit=True
        rubbish_shakespeare+=(format(output_text))

    punctRand = r.randint(1,4)
    if (punctRand==1):
        rubbish_shakespeare+="?\n"
    elif (punctRand==2):
        rubbish_shakespeare+="!\n"
    else:
        rubbish_shakespeare+=".\n"
    return rubbish_shakespeare

# processAndSaveToPickle()
# sys.exit()
word_after_dict = loadPickle('shakespeare.pickle')
print(generateRubbishShakespeare(word_after_dict))
