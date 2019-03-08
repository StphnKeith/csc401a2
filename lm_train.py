from preprocess import *
import pickle
import os

def lm_train(data_dir, language, fn_LM):
    """
    This function reads data from data_dir, computes unigram and bigram counts,
    and writes the result to fn_LM
    
    INPUTS:
    
    data_dir    : (string) The top-level directory continaing the data from which
                    to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
    language    : (string) either 'e' (English) or 'f' (French)
    fn_LM       : (string) the location to save the language model once trained
    
    OUTPUT
    
    LM          : (dictionary) a specialized language model
    
    The file fn_LM must contain the data structured called "LM", which is a dictionary
    having two fields: 'uni' and 'bi', each of which holds sub-structures which 
    incorporate unigram or bigram counts
    
    e.g., LM['uni']['word'] = 5         # The word 'word' appears 5 times
          LM['bi']['word']['bird'] = 2  # The bigram 'word bird' appears 2 times.
    """
    
    # TODO: Implement Function
    # Instantiate a unigram dictionary
    # Instantiate a bigram dictionary of dictionaries
    # For each file appended with language:
        # Load preprocessed lines into a list
        # For each word in the line:
            # NOTE: include SENTSTART and punctuation, include SENTEND in the
                # unigram and in the second word of the bigrams
            # If the word is not in the unigram dictionary:
                # add it and set its count to 1
            # Else increment its count by 1
            # If the word is SENTEND, continue (i.e. end the line loop)
            # Elif the word and the word after it aren't in the bigram dict:
                # add them and set their count to 1
            # Else increment their count by 1

    # language_model = { 'uni': uni_dict, 'bi': bi_dict }

    unigram = {}
    bigram = {}

    files = os.listdir(data_dir)
    for file in files:
        # Validate extension
        file_name, extension = os.path.splitext(file)
        if not extension == ('.' + language):
            continue

        file_path = os.path.join(data_dir, file)
        with open(file_path) as lines:
            for line in lines:
                words = preprocess(line.rstrip(), language).split()
                for i in range(0,len(words) - 1):
                    word = words[i]
                    next_word = words[i+1]

                    if word not in unigram:
                        unigram[word] = 1
                    else:
                        unigram[word] += 1

                    if word not in bigram:
                        bigram[word] = {next_word: 1}
                    else:
                        if next_word not in bigram[word]:
                            bigram[word][next_word] = 1
                        else:
                            bigram[word][next_word] += 1

                word = words[len(words)]
                if word not in unigram:
                    unigram[word] = 1
                else:
                    unigram[word] += 1

    language_model = { 'uni': uni_dict, 'bi': bi_dict }

    #Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    return language_model