from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.sparse import hstack
import pickle
import pandas as pd
import numpy as np

def gen_stylo(df, col):  # col should be the original (translated) tweet column
    assert isinstance(col, pd.Series), "Input data is not a pandas series, it is of type " + str(type(col))
    assert isinstance(df, pd.DataFrame), "Input data is not a pandas df, it is of type " + str(type(col))
    texts = np.array(col)
    # sentiment
    analyzer = SentimentIntensityAnalyzer()

    sentiment = []

    for text in texts:
        sentiment.append(analyzer.polarity_scores(text)["compound"])

    return sentiment

def generate(DATAPATH):
    # unpack fitted vectorizer
    with open('./model/vectorizer', 'rb') as fin:
        pickled_vz = pickle.load(fin)

    val = pd.read_csv(DATAPATH)
    test_transformed = pickled_vz.transform(val["cleaned"].values.astype("U"))  # test set transformed

    # generate add features.
    val["sentiment"] = gen_stylo(val, val["translated"])
    # Join vectorised with new features
    test_transformed = hstack((test_transformed, np.array(val["sentiment"])[:, None])).tocsr()

    return test_transformed

def predict(transformed, LOADPATH, SAVEPATH):
    with open('./model/SVCmodel', 'rb') as fin:
        pickled_model = pickle.load(fin)

    temp = pickled_model.predict(transformed)

    predicted = pd.read_csv(LOADPATH)
    predicted["predicted"] = temp
    predicted.to_csv(SAVEPATH, encoding='utf-8-sig')

    return predicted

#DATA_PATH = './input_data/tweets.csv'

#print(predict(generate(DATA_PATH), DATA_PATH, './outputs/results/results.csv'))
