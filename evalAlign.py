#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import _pickle as pickle

import decode
from align_ibm1 import *
from BLEU_score import *
from lm_train import *
from perplexity import *

__author__ = 'Raeid Saqur'
__copyright__ = 'Copyright (c) 2018, Raeid Saqur'
__email__ = 'raeidsaqur@cs.toronto.edu'
__license__ = 'MIT'


discussion = """
Discussion :

{Enter your intriguing discussion (explaining observations/results) here}

"""

##### HELPER FUNCTIONS ########
def _getLM(data_dir, language, fn_LM, use_cached=True):
    """
    Parameters
    ----------
    data_dir    : (string) The top-level directory continaing the data from which
                    to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
    language    : (string) either 'e' (English) or 'f' (French)
    fn_LM       : (string) the location to save the language model once trained
    use_cached  : (boolean) optionally load cached LM using pickle.

    Returns
    -------
    A language model 
    """
    if use_cached:
        with open(fn_LM, 'rb') as file:
            LM = pickle.load(file)
    else:
        LM = lm_train(data_dir, language, fn_LM)
    return LM

def _getAM(data_dir, num_sent, max_iter, fn_AM, use_cached=True):
    """
    Parameters
    ----------
    data_dir    : (string) The top-level directory continaing the data 
    num_sent    : (int) the maximum number of training sentences to consider
    max_iter    : (int) the maximum number of iterations of the EM algorithm
    fn_AM       : (string) the location to save the alignment model
    use_cached  : (boolean) optionally load cached AM using pickle.

    Returns
    -------
    An alignment model 
    """
    if use_cached:
        with open(fn_AM, 'rb') as file:
            AM = pickle.load(file)
    else:
        AM = align_ibm1(data_dir, num_sent, max_iter, fn_AM)
    return AM

def _get_BLEU_scores(eng_decoded, eng, google_refs, n):
    """
    Parameters
    ----------
    eng_decoded : an array of decoded sentences
    eng         : an array of reference handsard
    google_refs : an array of reference google translated sentences
    n           : the 'n' in the n-gram model being used

    Returns
    -------
    An array of evaluation (BLEU) scores for the sentences
    """
    # I'm going to assume they mean list when they say array.
    length = min(len(eng_decoded), len(eng), len(google_refs))
    bleu_scores = [1] * length
    for i in range(0,length):
        references = [eng[i], google_refs[i]]
        candidate = eng_decoded[i]

        for j in range(1,n+1):
            bleu_scores[i] *= BLEU_score(candidate, references, j)

        bleu_scores[i] = bleu_scores[i] ** (1/n)
        bleu_scores[i] *= brevity_penalty(candidate, references)

    return bleu_scores
   

def main(args):
    """
    #TODO: Perform outlined tasks in assignment, like loading alignment
    models, computing BLEU scores etc.

    (You may use the helper functions)

    It's entirely upto you how you want to write Task5.txt. This is just
    an (sparse) example.
    """
    

    ## Write Results to Task5.txt (See e.g. Task5_eg.txt for ideation). ##

    '''
    f = open("Task5.txt", 'w+')
    f.write(discussion) 
    f.write("\n\n")
    f.write("-" * 10 + "Evaluation START" + "-" * 10 + "\n")

    for i, AM in enumerate(AMs):
        
        f.write(f"\n### Evaluating AM model: {AM_names[i]} ### \n")
        # Decode using AM #
        # Eval using 3 N-gram models #
        all_evals = []
        for n in range(1, 4):
            f.write(f"\nBLEU scores with N-gram (n) = {n}: ")
            evals = _get_BLEU_scores(...)
            for v in evals:
                f.write(f"\t{v:1.4f}")
            all_evals.append(evals)

        f.write("\n\n")

    f.write("-" * 10 + "Evaluation END" + "-" * 10 + "\n")
    f.close()
    '''

    # Task 3
    # Record into Task3.txt (or print) (for each language):
        # Perplexity of /u/cs401/A2_SMT/data/Hansard/Testing/ with:
            # no smoothing
            # delta = 0.2
            # delta = 0.4
            # delta = 0.6
            # delta = 0.8
            # delta = 1.0

    print("Task 3")
    print("Training English")
    LM_e = _getLM('/u/cs401/A2_SMT/data/Hansard/Training', 'e', 'LM_e', use_cached=False)
    print("Training French")
    LM_f = _getLM('/u/cs401/A2_SMT/data/Hansard/Training', 'f', 'LM_f', use_cached=False)
    t3 = []
    for lm in [(LM_e, 'e'), (LM_f, 'f')]:
        perps = []
        print("Perplexity for " + lm[1])
        perps.append(preplexity(lm[0], '/u/cs401/A2_SMT/data/Hansard/Testing', lm[1], smoothing = False, delta = 0))
        for d in [0.2, 0.4, 0.6, 0.8, 1.0]:
            perps.append(preplexity(lm[0], '/u/cs401/A2_SMT/data/Hansard/Testing', lm[1], smoothing = True, delta = d))
        t3.append(perps)

    k = 0
    with open("Task3.txt", 'w') as file:
        for line in t3:
            if k == 0:
                file.write('e\n')
            else:
                file.write('f\n')
            file.write(str(line) + '\n')
            k += 1

    # Task 5
    # AMs = []
    # For each num_sentences in [1000, 10000, 15000, 30000]:
        # Train AM on num_sentences
            # AM = align_ibm1('/u/cs401/A2_SMT/data/Hansard/Training/', num_sentences, 1000, "align" + str(num_sentences))
            # AMs.append(AM)
        # Iterate through lines in Task5.f, Task5.e, and Task5.google.e
        # simultaneously and put them in three lists
        # Make sure to preprocess them as you iterate
        # bleu_scores = []
        # for n in range(1,4):
            # call _get_BLEU_scores on the lists with n to get score
            # bleu_scores.append(score)
    # Finally write bleu_scores to Task5.txt

    print("Task 5")
    french = []
    with open('/u/cs401/A2_SMT/data/Hansard/Testing/Task5.f') as file:
        for line in file:
            french.append(preprocess(line, 'f'))

    hansard = []
    with open('/u/cs401/A2_SMT/data/Hansard/Testing/Task5.e') as file:
        for line in file:
            hansard.append(preprocess(line, 'e'))

    google = []
    with open('/u/cs401/A2_SMT/data/Hansard/Testing/Task5.google.e') as file:
        for line in file:
            google.append(preprocess(line, 'e'))

    bleu_scores = []
    MAX_ITER = 50
    for num_sentences in [1000, 10000, 15000, 30000]:
        print("Align " + str(num_sentences))
        AM = align_ibm1('/u/cs401/A2_SMT/data/Hansard/Training/', num_sentences, MAX_ITER, "align" + str(num_sentences))
        print("Decoding")
        english = []
        for f in french:
            english.append(decode.decode(f, LM_e, AM))
        print("Getting bleu scores for " + str(num_sentences))
        for n in range(1,4):
            score = _get_BLEU_scores(english, hansard, google, n)
            bleu_scores.append(score)

    i = 1
    j = 0
    lengths = [1000, 10000, 15000, 30000]
    with open("Task5.txt", 'w') as file:
        for line in bleu_scores:
            file.write(str(lengths[j]) + " " + str(((i-1)%3)+1) + '\n')
            file.write(str(line) + '\n')
            if (i % 3) == 0:
                j += 1
            i += 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use parser for debugging if needed")
    args = parser.parse_args()

    main(args)