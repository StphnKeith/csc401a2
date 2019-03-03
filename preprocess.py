import re

def preprocess(in_sentence, language):
    """ 
    This function preprocesses the input text according to language-specific rules.
    Specifically, we separate contractions according to the source language, convert
    all tokens to lower-case, and separate end-of-sentence punctuation 
	
	INPUTS:
	in_sentence : (string) the original sentence to be processed
	language	: (string) either 'e' (English) or 'f' (French)
				   Language of in_sentence
				   
	OUTPUT:
	out_sentence: (string) the modified sentence
    """
    # TODO: Implement Function
	# separate sentence-final punctuation
    # separate commas, colons, semicolons, parentheses, dashes,
    # mathematical ops (+, -, <, >, =), and quotation marks
    # add SENTSTART and SENTEND to the end of the sentence

    # when language == 'f' separate the following contractions:
        # leading l' from concatenated word: l'election => l' election
        # leading consonant and apostraphe from concatenated word: j'ai => j' ai
        # leading qu' from concatenated word: qu'on => qu' on
        # following on or il: puisqu'on => puisqu' on, lorsqu'il => lorsqu' il
    # any words containing apostraphes not described above can be left as is
    # the following words should not be separated:
        # d'abord, d'accord, d'ailleurs, d'habitude

    return out_sentence
