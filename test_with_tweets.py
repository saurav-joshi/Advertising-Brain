#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow as tf
import data_helpers
from cnn_text_with_embeddings import TextCNN
import tweets_cleaner as cleaner
import ast
import data_helpers
#import MySQLdb
import pandas as pd
from nltk.tokenize import TweetTokenizer,casual
import csv
import logging
import os
import pickle
import clean_tags
import string
from sklearn.linear_model import SGDClassifier
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize

logger = logging.getLogger('apscheduler.executors.default')
hdlr = logging.FileHandler(os.path.join(os.path.curdir,'logs','myapp.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Model Hyperparameters
tf.flags.DEFINE_integer("embedding_dim", 200, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "2,3,4", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularizaion lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 2000, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS.batch_size
x_train, y_train, vocabulary,labels_dict,w2v_for_vocab = data_helpers.load_data(logger)
logger.info("Vocab loaded...")
#print labels_dict
#labels_dict = ast.literal_eval("{'travel': [0, 0, 0, 0, 1], 'fashion_style': [0, 0, 0, 1, 0], 'arts_ent': [0, 1, 0, 0, 0], 'food_drink': [0, 0, 1, 0, 0], 'sports': [1, 0, 0, 0, 0]}")
def tokenize(text):
    txt = "".join([ch for ch in text if ch not in string.punctuation])
    wnl = WordNetLemmatizer()
    return [wnl.lemmatize(t) for t in word_tokenize(txt)]

arts_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','arts & entertainment_vocab.pickle')))
arts_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','arts & entertainment_tfidf.pickle')))
arts_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','arts & entertainment_classifier.pickle')))

family_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','family & parenting_vocab.pickle')))
family_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','family & parenting_tfidf.pickle')))
family_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','family & parenting_classifier.pickle')))

fashion_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','fashion_vocab.pickle')))
fashion_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','fashion_tfidf.pickle')))
fashion_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','fashion_classifier.pickle')))

food_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','food & drink_vocab.pickle')))
food_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','food & drink_tfidf.pickle')))
food_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','food & drink_classifier.pickle')))

hobbies_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','hobbies & interests_vocab.pickle')))
hobbies_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','hobbies & interests_tfidf.pickle')))
hobbies_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','hobbies & interests_classifier.pickle')))

religion_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','religion & sprituality_vocab.pickle')))
religion_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','religion & sprituality_tfidf.pickle')))
religion_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','religion & sprituality_classifier.pickle')))

science_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','science_vocab.pickle')))
science_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','science_tfidf.pickle')))
science_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','science_classifier.pickle')))

society_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','society_vocab.pickle')))
society_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','society_tfidf.pickle')))
society_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','society_classifier.pickle')))

sports_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','sports_vocab.pickle')))
sports_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','sports_tfidf.pickle')))
sports_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','sports_classifier.pickle')))

technology_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','technology & computing_vocab.pickle')))
technology_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','technology & computing_tfidf.pickle')))
technology_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','technology & computing_classifier.pickle')))

travel_vocab_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','travel_vocab.pickle')))
travel_tfidf_pickle = pickle.load(open(os.path.join(os.path.curdir,'resources','travel_tfidf.pickle')))
travel_clf = pickle.load(open(os.path.join(os.path.curdir,'resources','travel_classifier.pickle')))


def fetch_vocab(category):
    if category == 'arts & entertainment':
        return arts_vocab_pickle,arts_tfidf_pickle,arts_clf
    elif category == 'family & parenting':
        return family_vocab_pickle,family_tfidf_pickle,family_clf
    elif category == 'fashion':
        return fashion_vocab_pickle,fashion_tfidf_pickle,fashion_clf
    elif category == 'food & drink':
        return food_vocab_pickle,food_tfidf_pickle,food_clf
    elif category == 'hobbies & interests':
        return hobbies_vocab_pickle,hobbies_tfidf_pickle,hobbies_clf
    elif category == 'religion & sprituality':
        return religion_vocab_pickle,religion_tfidf_pickle,religion_clf
    elif category == 'science':
        return science_vocab_pickle,science_tfidf_pickle,science_clf
    elif category == 'society':
        return society_vocab_pickle,society_tfidf_pickle,society_clf
    elif category == 'sports':
        return sports_vocab_pickle,sports_tfidf_pickle,sports_clf
    elif category == 'technology & computing':
        return technology_vocab_pickle,technology_tfidf_pickle,technology_clf
    elif category == 'travel':
        return travel_vocab_pickle,travel_tfidf_pickle,travel_clf

tknzr = TweetTokenizer(reduce_len=True)

def find_subcategory(first_category,tweet):
    vocab_pickle,tfidf_pickle,clf = fetch_vocab(first_category.lower())

    tweet = [clean_tags.clean(' '.join(tknzr.tokenize(tweet.decode('utf-8','ignore')))).replace('<hashtag>', '').replace('<allcaps>', '')]
    tweet=[t.encode('utf-8').translate(string.maketrans("",""), string.punctuation) for t in tweet]

    X_new_counts = vocab_pickle.transform(tweet)
    X_new_tfidf = tfidf_pickle.transform(X_new_counts)
    subcategory_prediction = clf.predict(X_new_tfidf)
    return subcategory_prediction[0]


def classify_tweets():

    logger.info("Classification begins .....")
    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            cnn = TextCNN(
                sequence_length=x_train.shape[1],
                num_classes=len(labels_dict),
                vocab_size=len(vocabulary),
                embedding_size=FLAGS.embedding_dim,
                filter_sizes=map(int, FLAGS.filter_sizes.split(",")),
                num_filters=FLAGS.num_filters,
                w2v_for_vocab = w2v_for_vocab,
                l2_reg_lambda=FLAGS.l2_reg_lambda)
            saver = tf.train.Saver()

            #saver.restore(sess,"/home/srinath/tweets_classifier/runs/1465888679/checkpoints/model-14200")
        saver.restore(sess,os.path.join(os.path.curdir,'resources','model-20400'))

        df = pd.read_csv(os.path.join(os.path.curdir,'resources','july_27.csv'),header=None, error_bad_lines=False)

        with open(os.path.join(os.path.curdir,'results','real_test.csv'), 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["tweet","first_pred","first_score","second_pred","second_score","subcategory"])

            for eachRow in df.iterrows() :
                #try:
                if type(eachRow[1][4]) == str:
                    tweet = eachRow[1][4].strip()
                    tknzr = TweetTokenizer(reduce_len=True)
                    input_txt=cleaner.clean(' '.join(tknzr.tokenize(tweet.decode('utf-8','ignore'))))

                    x_user = data_helpers.create_vec_for_prod_data(input_txt,x_train.shape[1],vocabulary)
                    feed_dict = {
                          cnn.input_x: x_user,

                          cnn.dropout_keep_prob: 1.0
                        }

                    prediction = sess.run(cnn.predictions,feed_dict)
                    scores = sess.run(cnn.scores,feed_dict)

                    first_predict = prediction
                    second_predict = scores.tolist()[0].index(sorted(scores.tolist()[0],reverse=True)[1])
                    for k in labels_dict.keys():
                        if labels_dict[k][first_predict] == 1:
                            first_category = k
                            first_cat_score = scores.tolist()[0][first_predict]
                        elif labels_dict[k][second_predict] == 1:
                            second_category = k
                            second_cat_score = scores.tolist()[0][second_predict]

                    subcategory=find_subcategory(first_category,tweet)
                    spamwriter.writerow([tweet,first_category,first_cat_score,second_category,second_cat_score,subcategory])

    logger.info("Classification completed !!")


def test_fn():
    print "I am  working"
if __name__ == '__main__':
    classify_tweets()
    test_fn()

