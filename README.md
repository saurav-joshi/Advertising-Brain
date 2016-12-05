# Advertising-Brain
Capstone project for Udacity Machine Learning Engineer nanodegree

# Environment Setup:
Python: 2.7.11
java version: 1.8.0_65

# Install Anaconda and download NLTK:
wget http://repo.continuum.io/archive/Anaconda2-4.1.0-Linux-x86_64.sh
bash ~/Downloads/Anaconda2-4.1.0-Linux-x86_64.sh
nltk.download()


# Install Tensorflow:
https://www.tensorflow.org/versions/r0.12/get_started/os_setup.html#pip-installation


# Download Stanford NLP jars and place them under resources directory:
https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software


# Install CLIFF that allows HTTP requests to the Stanford Named Entity Recognizer
https://github.com/c4fcm/CLIFF


# Download GloVe for twitter - Global Vectors for Word Representation
http://nlp.stanford.edu/projects/glove/




# Steps for training, classification and entity extraction from tweets


# Training:

     1. Run train_with_tweets.py as ./train_with_tweets.py
           This trains the CNN for the given training data in the folder training_data

     2. Place the model generated from the path
          /runs/1464942336/checkpoints/model-24800 to resources folder

     3. Classification:
        Run test_with_tweets.py as ./test_with_tweets.py that will run the trained model and classify the twees and writes the classified tweets into results folder


     4. Entity extraction:
        RUN insights_twitter.py as ./insights_twitter.py that will extract entities and writes them to files such as corelation.csv, entities.csv, hashtags.csv and phrases.csv




# Sample output:
The output of the above process can be visualized in the below links


# Corelation between different categories
https://www.google.com/fusiontables/DataSource?docid=1L4SklcpYnTC-w7ccBDfXVgJ7c2av7OYbYAiCeovZ


# Entities:
https://www.google.com/fusiontables/DataSource?docid=18ei6Kfr2awq7yjbp1bQWRVwtOXJP9rT4uumwil8_


# Hashtags:
https://www.google.com/fusiontables/DataSource?docid=1PwNVA6ZXwXxSJE6qfd7l0efM5aCVXB-bgpmgaRsk


# Phrases:
https://www.google.com/fusiontables/DataSource?docid=1FDsxuvV_D5R6WnINj7oIHsZe1hyGkuSNTGSGFavs

