import re
import string
import numpy as np


def clean_text(text):
    # remove numbers and words with numbers
    text_nonum = re.sub(r'\w*\d+', '', text)
    # remove punctuations and convert characters to lower case
    text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation])
    # substitute multiple whitespace with single whitespace
    # Also, removes leading and trailing whitespaces
    text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
    text_no_one_letter_words = re.sub('\s\w\s', '', text_no_doublespace)
    return re.sub('^\w\s', '', text_no_one_letter_words)


def get_phrase_embedding(phrase, model, tokenize_method):
    """
    Convert phrase to a vector by aggregating it's word embeddings.
    """
    # 1. lowercase phrase
    # 2. tokenize phrase
    # 3. average word vectors for all words in tokenized phrase
    # skip words that are not in model's vocabulary
    # if all words are missing from vocabulary, return zeros

    vector = np.empty((0, model.vector_size), dtype='float32')

    for word in tokenize_method(phrase)[:6]:
        if word in model.key_to_index:
            vector = np.append(vector, np.array([model.get_vector(word)]), axis=0)

    if vector.shape[0] == 0:
        return np.zeros([model.vector_size], dtype='float32')
    else:
        return np.mean(vector, axis=0)
