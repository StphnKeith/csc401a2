from lm_train import *
from log_prob import *
from preprocess import *
from math import log
import os

def align_ibm1(train_dir, num_sentences, max_iter, fn_AM):
    """
    Implements the training of IBM-1 word alignment algoirthm. 
    We assume that we are implemented P(foreign|english)
    
    INPUTS:
    train_dir :     (string) The top-level directory name containing data
                    e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
    num_sentences : (int) the maximum number of training sentences to consider
    max_iter :      (int) the maximum number of iterations of the EM algorithm
    fn_AM :         (string) the location to save the alignment model
    
    OUTPUT:
    AM :            (dictionary) alignment model structure
    
    The dictionary AM is a dictionary of dictionaries where AM['english_word']['foreign_word'] 
    is the computed expectation that the foreign_word is produced by english_word.
    
            AM['house']['maison'] = 0.5
    """
    AM = {}
    
    # Read training data
    eng, fre = read_hansard(train_dir, num_sentences)
    
    # Initialize AM uniformly
    AM = initialize(eng, fre)
    
    # Iterate between E and M steps
    for i in range(0, max_iter):
        AM = em_step(AM, eng, fre)

    return AM
    
# ------------ Support functions --------------
def read_hansard(train_dir, num_sentences):
    """
    Read up to num_sentences from train_dir.
    
    INPUTS:
    train_dir :     (string) The top-level directory name containing data
                    e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
    num_sentences : (int) the maximum number of training sentences to co

    
    Make sure to preprocess!
    Remember that the i^th line in fubar.e corresponds to the i^th line in fubar.f.
    
    Make sure to read the files in an aligned manner.
    """
    """
    # TODO
    # Get starting files from directory:
        # Get file num
        # If file language is english get french with same num, & vice versa
        # load files into two lists: curr_english, curr_french
    # while count < num_sentences:
        # if index >= len(curr_english):
            # load two new files into curr_english and curr_french
            # make sure to keep track of files already read
            # index = 0        
        # sentences['e'][count] = preprocess(curr_english[index])
        # sentences['f'][count] = preprocess(curr_french[index])

    #====================================
    # Return (eng, fre) version:
    # Get starting files from directory:
        # Get file num
        # If file language is english get french with same num, & vice versa
        # load files into two lists: curr_english, curr_french
    # while count < num_sentences:
        # if index >= min(len(curr_english), len(curr_french)):
            # load two new files into curr_english and curr_french
            # make sure to keep track of files already read
            # index = 0
        # preprocess and remove SENTSTART and SENTEND from the sentences
        # eng[count] = eng_sentence.split()
        # fre[count] = fre_sentence.split()
    # return (eng, fre)
    """

    files_examined = set()
    count = 0
    eng = []
    fre = []

    # for subdir, dirs, files in os.walk(train_dir):
    #     for file in files:

    files = os.listdir(train_dir)
    for file in files:

        # First set up and validate the files
        file_name, extension = os.path.splitext(file)
        file_name, file_id = os.path.splitext(file_name)

        # Skip if not .e or .f file
        if not (extension == '.f' or extension == '.e'):
            continue

        # Skip if already examined this file pair
        if file_id in files_examined:
            continue

        # Skip if either language file is not available
        eng_file = file_name + file_id + '.e'
        fre_file = file_name + file_id + '.f'
        if eng_file not in files or fre_file not in files:
            continue

        # If it reaches here we know we can process it
        files_examined.add(file_id)
        print( "Processing " + file_id)

        # Finally open files and iterate simultaneously
        eng_path = os.path.join(train_dir, eng_file)
        fre_path = os.path.join(train_dir, fre_file)
        with open(eng_path) as english:
            with open(fre_path) as french:
                for E, F in zip(english, french):

                    # Stop when limit reached
                    if count >= num_sentences:
                        return (eng, fre)

                    # Process and split sentences
                    E = preprocess(E.rstrip(), 'e')
                    F = preprocess(F.rstrip(), 'f')

                    E_words = E.split()
                    F_words = F.split()

                    eng.append(E_words)
                    fre.append(F_words)

                    count += 1

    return (eng, fre)

def initialize(eng, fre):
    """
    Initialize alignment model uniformly.
    Only set non-zero probabilities where word pairs appear in corresponding sentences.
    """
    # TODO
    # Setup keys of AM
    # For each sentence pair:
        # For each word in english:
            # If eng_word is not in AM:
                # AM[eng_word] = {}
            # For each word in french:
                # AM[eng_word][french_word] = 0

    # Setup values of AM
    # For each word in english in AM:
        # AM[eng_word] = dict.fromkeys( AM[eng_word], 1 / len(AM[eng_word]) )

    # Force SENTEND and SENTSTART

    #============================
    # initialize(eng, fre) version:
    # presumably we return an AM dictionary
    # the algorithm is the same as above we just iterate over lists of words
    # rather than words in a sentence string

    AM = {}

    num_sentences = min(len(eng), len(fre))
    for i in range(0, num_sentences):
        for e in eng[i]:
            if e not in AM:
                AM[e] = {}
            for f in fre[i]:
                AM[e][f] = 0

    for e in AM.keys():
        AM[e] = dict.fromkeys( AM[e], 1 / len(AM[e]) )

    if 'SENTSTART' in AM.keys() and 'SENTEND' in AM.keys():
        AM['SENTSTART'] = dict.fromkeys(AM['SENTSTART'], 0)
        AM['SENTSTART']['SENTSTART'] = 1
        AM['SENTEND'] = dict.fromkeys(AM['SENTEND'], 0)
        AM['SENTEND']['SENTEND'] = 1

    return AM
    
def em_step(t, eng, fre):
    """
    One step in the EM algorithm.
    Follows the pseudo-code given in the tutorial slides.
    """
    # TODO
    # Lecture Steps:
        # 1. Make a table of P(f|e) for all possible pairs of f and e, prob_tab
        # 2. Make a grid where each sentence pair is a row and each possible
        #    alignment is a column
        # 3. For each sentence pair and alignment compute P(F|a,E)
        #    Given aligned words f1,f2,...,fn and e1,e2,...,en in the pair:
        #    P(F|a,E) = prob_tab[f1][e1] * ... * prob_tab[fn][en]
        # 4. For each sentence pair and alignment
        #    divide P(F|a,E) by the sum of the P(F|a,E)'s in the row
        #    this is P(a|E,F)
        # 5. For each possible word pair e and f, sum P(a|E,F) across all
        #    alignments and sentence pairs for each instance that e is aligned
        #    with f, this gets out a TCount table
        # 6. Sum over the rows of TCount to get the total estimates for each
        #    english word e.
        # 7. Compute P(f|e) = TCount[f][e] / Total[e]
        #    This is the model after 1 iteration.

    '''
    Tutorial Steps:
    initialize P(f|e)
    for a number of iterations:
        set tcount(f, e) to 0 for all f, e
        set total(e) to 0 for all e
        for each sentence pair (F, E) in training corpus:
            for each unique word f in F:
                denom_c = 0
                for each unique word e in E:
                    denom_c += P(f|e) * F.count(f)
                for each unique word e in E:
                    tcount(f, e) += P(f|e) * F.count(f) * E.count(e) / denom_c
                    total(e)     += P(f|e) * F.count(f) * E.count(e) / denom_c
        for each e in domain(total(:)):
            for each f in domain(tcount(:,e)):
                P(f|e) = tcount(f, e) / total(e)
    '''

    '''
    My Pseudocode:
    The Table of P(f|e) is already initiated as the AM dictionary.
    Presumably the AM is passed in as t.
    Initialize TCount as a dictionary like AM, e.g. TCount[e][f] = 0
    Initialize Total as a dictionary with the same entries as TCount[e] = 0
    for i in range(0,len(eng)):

    '''
    AM = dict.fromkeys(t.keys(), 0)
    Total = dict.fromkeys(t.keys(), 0)
    TCount = dict.fromkeys(t.keys(), 0)
    for key in TCount.keys():
        TCount[key] = dict.fromkeys(t[key].keys(), 0)
        AM[key] = dict.fromkeys(t[key].keys(), 0)

    num_sentences = min(len(eng), len(fre))
    for i in range(0, num_sentences):
        E = eng[i]
        F = fre[i]
        E_uniques = list(set(E))
        F_uniques = list(set(F))
        for f in F_uniques:
            denom_c = 0
            for e in E_uniques:
                denom_c += t[e][f] * F.count(f)
            for e in E_uniques:
                TCount[e][f] += t[e][f] * F.count(f) * E.count(e) / denom_c
                Total[e] += t[e][f] * F.count(f) * E.count(e) / denom_c
    for e in Total.keys():
        for f in TCount[e].keys():
            AM[e][f] = TCount[e][f] / Total[e]

    return AM
