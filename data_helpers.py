from nltk.tokenize import TweetTokenizer,casual
import nltk
import pandas as pd
import re
import numpy as np
import itertools
import collections
import csv
import tweets_cleaner as cleaner
import pickle
import os


def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`<>]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def create_vec_for_prod_data(text,seq_len,vocabulary):
    x_text = clean_str(text)
    x_text = x_text.split(" ")

    padded_sentences = []
    for sent in [x_text]:
        if len(sent) < seq_len:
            sent = sent + ["<PAD/>"]*(seq_len-len(sent))
            padded_sentences.append(sent)
        else:
            padded_sentences.append(sent)

    sentences_padded = padded_sentences

    x = np.array([[vocabulary[word] if word in vocabulary else vocabulary["<PAD/>"] for word in sentence ] for sentence in sentences_padded])

    return x


def load_data_and_labels():

    df=pd.read_csv(os.path.join(os.path.curdir,'training_data','training_tweets.csv'))
    tknzr = TweetTokenizer(reduce_len=True)

    x_text = [cleaner.clean(' '.join(tknzr.tokenize(text.decode('utf-8','ignore')))) for text in df['text'].tolist()]

    num_unique_labels = len(df['label'].unique())
    labels = df['label'].unique()

    print num_unique_labels

    # Split by words
    x_text = [clean_str(raw_sent) for raw_sent in x_text]
    x_text = [clean_sent.split(" ") for clean_sent in x_text]

    # Generate labels
    label_matrix = np.zeros((num_unique_labels,num_unique_labels),dtype=np.int)
    label_dict={}
    idx=0
    for l in labels:
        #print l
        label_matrix[idx][idx]=1
        label_dict[l]=label_matrix[idx].tolist()
        idx=idx+1
    #print label_dict

    full_label_matrix=[]
    for index, row in df.iterrows():
        full_label_matrix.append(label_dict[row['label']])


    y=np.array(full_label_matrix)

    return [x_text,y,label_dict]

def pad_sentences(sentences, padding_word="<PAD/>"):
    max_len = max(len(sent) for sent in sentences)

    padded_sentences = []
    for sent in sentences:
        if len(sent) < max_len:
            sent = sent + [padding_word]*(max_len-len(sent))
            padded_sentences.append(sent)
        else:
            padded_sentences.append(sent)

    return padded_sentences


def build_vocab(sentences):
    word_count = collections.Counter(itertools.chain.from_iterable(sentences))

    common_words = word_count.most_common()
    common_words = [(tup[0],tup[1]) for tup in common_words if tup[1]>=3]

    words = [w[0] for w in common_words]

    vocab = {word:index for index,word in enumerate(words)}
    return [vocab,words]


def build_vectors_from_vocab(sentences,vocab,labels):
    x = np.array([[vocab[word] if word in vocab else vocab["<PAD/>"] for word in sentence] for sentence in sentences])

    y = np.array(labels)

    return [x,y]


def load_data(logger):
    """
    Loads and preprocessed data for the MR dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # Load and preprocess data
    if not os.path.exists(os.path.join(os.path.curdir,'resources','data_labels_w2v.pickle')):
        logger.info("Creating data, labels, w2v pickle ....")
        sentences, labels,labels_dict = load_data_and_labels()
        sentences_padded = pad_sentences(sentences)
        vocabulary, vocabulary_inv = build_vocab(sentences_padded)
        x, y = build_vectors_from_vocab(sentences_padded,vocabulary,labels)

        w2v = pd.read_csv(os.path.join(os.path.curdir,'resources','glove.twitter.27B.200d.txt'), header=None, delim_whitespace=True,quoting=csv.QUOTE_NONE)
        w2v = w2v.set_index([0])
        keys_to_be_fetched = []
        for i in xrange(len(vocabulary)):
            for k, v in vocabulary.iteritems():
                if v == i:
                    keys_to_be_fetched.append(k)

        w2v_for_vocab_df = w2v.ix[keys_to_be_fetched]
        w2v_for_vocab=w2v_for_vocab_df.as_matrix()
        idxs = np.where(np.isnan(w2v_for_vocab))
        w2v_for_vocab[idxs]=np.random.uniform(-1.0,1.0)
        del w2v

        data_labels_w2v = [x, y, vocabulary, labels_dict,w2v_for_vocab]
        logger.info("Vocab size: "+str(len(vocabulary)))
        logger.info(vocabulary)
        logger.info("Labels: "+str(labels_dict))
        logger.info("Word2Vec size: "+str(len(w2v_for_vocab)))


        with open(os.path.join(os.path.curdir,'resources','data_labels_w2v.pickle'), 'wb') as handle:
            pickle.dump(data_labels_w2v,handle)

        return data_labels_w2v
    else:
        logger.info("Loading pickle ....")

        with open(os.path.join(os.path.curdir,'resources','data_labels_w2v.pickle'), 'rb') as handle:
            data_labels_w2v = pickle.load(handle)
        #logger.info("Vocab size: "+str(len(data_labels_w2v[2])))
        #logger.info(data_labels_w2v[2])
        #logger.info("Labels: "+str(data_labels_w2v[4]))
        #logger.info("Word2Vec size: "+str(len(data_labels_w2v[5])))

        return data_labels_w2v


def batch_iter(data, batch_size, num_epochs):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size) + 1
    for epoch in xrange(num_epochs):
        # Shuffle the data at each epoch
        shuffle_indices = np.random.permutation(np.arange(data_size))
        shuffled_data = data[shuffle_indices]
        for batch_num in xrange(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


if __name__ == "__main__":
    x_text,y,label_dict = load_data_and_labels()

    print x_text[:10]
    print "----"
    print y[:10]
    print label_dict
