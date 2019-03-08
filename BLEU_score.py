import math

def brevity_pentalty(candidate, references):
    cand_words = candidate.split()

    BP = 1
    
    # Get length of candidate
    candidate_length = len(cand_words)

    # Find nearest length of references
    clostest_length = len(references[0].split())
    min_dist = abs( candidate_length - clostest_length )
    for ref in references:
        ref_length = len(ref.split())
        dist = abs(candidate_length - ref_length)

        if dist < min_dist:
            min_dist = dist
            clostest_length = ref_length
        elif dist == min_dist and ref_length < clostest_length:
            # This breaks ties in preference of the lower length reference
            min_dist = dist
            clostest_length = ref_length

    if clostest_length >= candidate_length:
        BP = math.e ** ( 1 - (clostest_length / candidate_length) )

    return BP

def BLEU_score(candidate, references, n, brevity=False):
    """
    Calculate the BLEU score given a candidate sentence (string) and a list of reference sentences (list of strings). n specifies the level to calculate.
    n=1 unigram
    n=2 bigram
    ... and so on
        
    DO NOT concatenate the measurments. N=2 means only bigram. Do not average/incorporate the uni-gram scores.
        
    INPUTS:
        candidate :  (string) Candidate sentence. "SENTSTART i am hungry SENTEND"
        references: (list) List containing reference sentences. ["SENTSTART je suis faim SENTEND", "SENTSTART nous sommes faime SENTEND"]
        n :         (int) one of 1,2,3. N-Gram level.

    
    OUTPUT:
    bleu_score :    (float) The BLEU score
    """
    
    #TODO: Implement by student.

    # There is no capping.
    # We have one candidate.
    cand_words = candidate.split()

    # Calculate the brevity penalty
    BP = 1
    if brevity:
        BP = brevity_pentalty(candidate, references)

    # Calculate N-Gram precision
    # For each N-Gram in candidate
        # For each reference
            # For each N-Gram in reference
                # record if N-Grams equal each other

    # Calculate N-Gram precision
    found_n_grams = [0] * (len(cand_words) - n + 1)

    # For each N-Gram in candidate
    for i in range(0,len(cand_words) - n + 1):
        n_gram = [cand_words[j] for j in range(i,i+n)]
        skip = False

        for ref in references:
            ref_words = ref.split()

            # For each N-Gram in ref
            for j in range(0,len(ref_words) - n + 1):
                ref_n_gram = [ref_words[k] for k in range(j,j+n)]

                # Check equality of N-Grams
                if n_gram == ref_n_gram:
                    found_n_grams[i] = 1

                    # Set skip to true to skip to next N-Gram
                    skip = True
                    break

            if skip:
                break

    n_gram_precision = sum(found_n_grams) / len(found_n_grams)
    bleu_score = BP * n_gram_precision
            
    return bleu_score
