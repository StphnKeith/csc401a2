from preprocess import *
from lm_train import *
from math import log

def log_prob(sentence, LM, smoothing=False, delta=0, vocabSize=0):
    """
    Compute the LOG probability of a sentence, given a language model and whether or not to
    apply add-delta smoothing
    
    INPUTS:
    sentence :  (string) The PROCESSED sentence whose probability we wish to compute
    LM :        (dictionary) The LM structure (not the filename)
    smoothing : (boolean) True for add-delta smoothing, False for no smoothing
    delta :     (float) smoothing parameter where 0<delta<=1
    vocabSize : (int) the number of words in the vocabulary
    
    OUTPUT:
    log_prob :  (float) log probability of sentence
    """
    
    #TODO: Implement by student.
    # If not smoothing, delta = 0
    # For each word in sentence:
        # Retrieve count of word, LM['uni'][word]
        # Retrieve count of bigram, LM['bi'][word][next_word]
        # If delta == 0 and bi_count == 0, log_prob = float('-inf')
        # Else:
            # est = (uni_count + delta) / ( bi_count + (delta * vocabSize) )
            # log_prob = log(est, 2)

    delta = 0 if not smoothing else delta

    # Since sentence is already processed, just split into words
    words = sentence.split()

    # No bigram to process for last word, so iterate length - 1
    for i in range(0,len(words) - 1):
        word = words[i]
        next_word = words[i+1]
        uni_count = LM['uni'][word]
        bi_count = LM['bi'][word][next_word]
        if delta == 0 and bi_count == 0:
            log_prob = float('-inf')
        else:
            est = (uni_count + delta) / ( bi_count + (delta * vocabSize) )
            log_prob = log(est, 2)

    return log_prob