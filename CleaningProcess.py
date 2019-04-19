import pandas as pd
import re, string, unicodedata
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

# this must be and gotten uploaded from App.py as df
df = pd.read_csv('datafiniti_hotel_reviews.csv')


# Cleaning of the DataFrame
def drop_columns():  # Delete columns that are not useful for our dataset
    # This is our feature selection - Reduce dimension
    dropcols = ['dateupdated', 'address', 'categories', 'keys',
                'dateadded', 'reviews_dateseen', 'reviews_sourceurls',
                'websites', 'location', 'reviews_username']
    return df.drop(dropcols)


def missing_val():  # Identifing missing values in the dataframe
    df.isnull().values.any()  # cristina
    df["reviews_text"].isna().sum()  # Kevin
    df["reviews_title"].notnull().isna().sum()  # Kevin
    df['reviews_text'] = df['reviews_text'].dropna().reset_index(drop=True)  # delete NaN and reindex   #cristina
    df['reviews_text'] = df['reviews_text'].astype(str)  # To assure all are strings #cristina


# Preprocessing Text Reviews
def text_to_analyze():  # DF with just title and the hotel review
    # text_df = df[['reviews_title', 'reviews_text']].copy()
    text_df = df["reviews_text"].copy()  # copy just the column text_reviews in a new DF #cristina
    return text_df


def preprocessing():
    df["reviews_text"] = df['reviews_text'].apply(lambda x: " ".join(x.lower() for x in x.split()))  # Lower case
    df["reviews_text"] = df["reviews_text"].str.replace('[^\w\s]', "")  # Remove Punctuation


def tokenization(text_df):  # tokenize into sentences #cristina
    df['reviews_text_token'] = df.apply(lambda row: nltk.word_tokenize(row['reviews_text']), axis=1)
    # l = text_df.shape[0]
    # for w in range(l):
    #     text_df[w] = word_tokenize(text_df[w])


def stop_words():  # Number of stopwords, needed to remove the stop word, but need to how many of them
    no_stops = [t for t in (df['reviews_text_token']) if
                t not in stopwords.words('english')]  # gets no stop words#cristina
    stop = set(stopwords.words('english'))
    df["stopwords_reviews_text"] = df["reviews_text"].apply(lambda x: len([x for x in str(x).split() if x in stop]))
    df["stopwords_reviews_title"] = df["reviews_title"].notnull().apply(
        lambda x: len([x for x in str(x).split() if x in stop]))


def remove_stop_w():  # Removal of Stop Words
    stop_words = stopwords.words('english')
    # df["reviews_text"] = df["reviews_text"].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # cristina #It removes stop_words and return an array filtered
    filtered_sent = []
    filtered_words = []
    for i in range(df.shape[0]):
        for w in df.loc[i, "reviews_text_token"]:
            if w not in stop_words:
                filtered_sent.append(w)
        filtered_words.append(filtered_sent)
        filtered_sent = []
    return filtered_words


def common_words():  # most frequent words #cristina
    for i in range(len(df['reviews_text_token'])):
        fdist = FreqDist(df.loc[i, "reviews_text_token"])
        print(fdist, fdist.most_common(10))


def cont_neg_feel():  # Number of Words (the negative sentiments contain
    # a lesser amount of words than the positive ones.)
    df["wordcount_reviews.text"] = df["reviews_text"].apply(lambda x: len(str(x).split(" ")))
    df["wordcount_reviews.title"] = df["reviews_title"].apply(lambda x: len(str(x).split(" ")))


def count_chr():  # Number of characters (includes spaces)
    df["charcount_reviews.text"] = df["reviews_text"].str.len()
    df["charcount_reviews.title"] = df["reviews_title"].str.len()


def avg_word(reviews):  # Average Word Length
    words = str(reviews).split()
    return (sum(len(word) for word in words) / len(words))
    df["avgword_reviews.text"] = df["reviews.text"].apply(lambda x: avg_word(x))
    df["avgword_reviews.title"] = df["reviews.title"].apply(lambda x: avg_word(x))


def NaivesB(): #performs classification, this algortithm uses probability #cristina
    y = df.label
    X_train, X_test, y_train, y_test = train_test_split(df['reviews_text'], y, test_size=0.25, random_state=53)
    count_vectorizer = CountVectorizer(stop_words='english')  # converts to bags of words and it would remove stop words
    count_train = count_vectorizer.fit_transform(X_train.values)
    count_test = count_vectorizer.transform(X_test.values)

    nb_classifier = MultinomialNB()
    nb_classifier.fit(count_train, y_train)
    pred = nb_classifier.predict(count_test)
    metrics.accuracy_score(y_test, pred)
    metrics.confusion_matrix(y_test, pred, labels=[1, 2, 3, 4, 5])

# #df = pd.read_csv("Datafiniti_Hotel_Reviews.csv")
# # df["reviews.text"] = df["reviews.text"].astype(str)
# # print(df.head())
# # print(df.dtypes)
# # print(df["reviews.text"].isna().sum())
# # print(df["reviews.title"].notnull().isna().sum())
# #
# # #Basic feature extraction using text data
# #
# # # Number of Words (the negative sentiments contain a lesser amount of words than the positive ones.)
# # df["wordcount_reviews.text"]=df["reviews.text"].apply(lambda x: len(str(x).split(" ")))
# # df["wordcount_reviews.title"]=df["reviews.title"].apply(lambda x: len(str(x).split(" ")))
# #
# # # Number of characters (includes spaces)
# # df["charcount_reviews.text"] = df["reviews.text"].str.len()
# # df["charcount_reviews.title"] = df["reviews.title"].str.len()
# #
# # # Average Word Length
# # def avg_word(reviews):
# #   words = str(reviews).split()
# #   return (sum(len(word) for word in words)/len(words))
# #
# # df["avgword_reviews.text"] = df["reviews.text"].apply(lambda x: avg_word(x))
# # df["avgword_reviews.title"] = df["reviews.title"].apply(lambda x: avg_word(x))
# #
# # # Number of stopwords, need to remove the stop word, but need to how many of them
# # import nltk
# # from nltk.corpus import stopwords
# # stop=stopwords.words('english')
# # df["stopwords_reviews.text"] = df["reviews.text"].apply(lambda x: len([x for x in str(x).split() if x in stop]))
# # df["stopwords_reviews.title"] = df["reviews.title"].notnull().apply(lambda x: len([x for x in str(x).split() if x in stop]))
# #
# # # Number of numerics
# # df["numerics_reviews.text"] = df["reviews.text"].apply(lambda x: len([x for x in str(x).split() if x.isdigit()]))
# # df["numerics_reviews.title"] = df["reviews.title"].apply(lambda x: len([x for x in str(x).split() if x.isdigit()]))
# #
# # # Number of Uppercase words (Anger or rage is quite often expressed by writing in UPPERCASE words )
# # df['upper_reviews.text'] = df['reviews.text'].apply(lambda x: len([x for x in str(x).split() if x.isupper()]))
# # df['upper_reviews.title'] = df['reviews.title'].apply(lambda x: len([x for x in str(x).split() if x.isupper()]))
# #
# # print(df[["reviews.text","wordcount_reviews.text","charcount_reviews.text","avgword_reviews.text","stopwords_reviews.text","numerics_reviews.text",'upper_reviews.text']].head())
# # print(df[["reviews.title","wordcount_reviews.title","charcount_reviews.title","avgword_reviews.title","stopwords_reviews.title","numerics_reviews.title",'upper_reviews.title']].head())
# #
# #
# # # Pre-processing
# #
# # #Lower case
# # df["reviews.text"] = df['reviews.text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
# # print(df['reviews.text'].head())
# #
# # #Remove Punctuation
# # df["reviews.text"] = df["reviews.text"].str.replace('[^\w\s]',"")
# # print(df['reviews.text'].head())
# #
# # #Removal of Stop Words
# # stop = stopwords.words('english')
# # df["reviews.text"] = df["reviews.text"].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
# # print(df["reviews.text"].head())
# #
# # #check the top ten common words, looks some of the common words may useful, we decide to retain for now.
# # freq = pd.Series(" ".join(df["reviews.text"]).split()).value_counts()[:10]
# # print(freq)
# #
# # #check the rare words, looks some of these words may cause by wrong spelling, so we decide to do the spelling correction
# # freq = pd.Series(" ".join(df["reviews.text"]).split()).value_counts()[-10:]
# # print(freq)
