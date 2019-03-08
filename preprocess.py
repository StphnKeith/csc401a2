import re

def preprocess(in_sentence, language):
    """ 
    This function preprocesses the input text according to language-specific rules.
    Specifically, we separate contractions according to the source language, convert
    all tokens to lower-case, and separate end-of-sentence punctuation 
    
    INPUTS:
    in_sentence : (string) the original sentence to be processed
    language    : (string) either 'e' (English) or 'f' (French)
                   Language of in_sentence
                   
    OUTPUT:
    out_sentence: (string) the modified sentence
    """
    # TODO: Implement Function
    # separate sentence-final punctuation
    # separate commas, colons, semicolons, parentheses, dashes,
    # mathematical ops (+, -, <, >, =), and quotation marks

    # when language == 'f' separate the following contractions:
        # leading l' from concatenated word: l'election => l' election
        # leading consonant and apostraphe from concatenated word: j'ai => j' ai
        # leading qu' from concatenated word: qu'on => qu' on
        # following on or il: puisqu'on => puisqu' on, lorsqu'il => lorsqu' il
    # any words containing apostraphes not described above can be left as is
    # the following words should not be separated:
        # d'abord, d'accord, d'ailleurs, d'habitude

    # add SENTSTART and SENTEND to the end of the sentence



    # Language universal stuff

    # Remove trailing whitespace, set to lower-case
    out_sentence = in_sentence.rstrip().lower()

    # Split end of sentence punctuation
    out_sentence = re.sub(r"((?:!|\?|\.)+)$", r" \1", out_sentence)

    # Split other odd punctuation and math symbols
    out_sentence = re.sub(r'((?:,|;|:|\(|\)|\[|\]|\{|\}|\+|-|<|>|=|")+)', r" \1 ", out_sentence)

    # French specific stuff
    if language == 'f':
        # Split l': l'election => l' election
        out_sentence = re.sub(r"(l')", r"\1 ", out_sentence)

        # Split 'silent e' consonants
        # (I don't know any french so I just cover what's in the handout)
        out_sentence = re.sub(r"(c'|t'|j')", r"\1 ", out_sentence)

        # Split qu'
        out_sentence = re.sub(r"(qu')", r"\1 ", out_sentence)

        # Split il or on following lorsqu' or puisqu'
        out_sentence = re.sub(r"(?<=puisqu'|lorsqu')(il|on)", r" \1", out_sentence)

    # Remove extraneous whitespace
    out_sentence = re.sub(r" +", " ", out_sentence).lstrip().rstrip()

    # Add SENTSTART and SENTEND
    out_sentence = "SENTSTART " + out_sentence + " SENTEND"

    return out_sentence
