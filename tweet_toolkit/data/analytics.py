import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime  as dt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from itertools import islice
import textacy.preprocessing.normalize as norm
import textacy.preprocessing.remove as remv
#lemma y frecuencia de uso por palabra no match (grafico-frecuencia) 10p, remover stopwords
    #subinstancia: la veces que se mencionan palabras especificas (grafico-frecuencia)

#grafico de referencias

class FrecuencyPlot:

    @staticmethod
    def general_distribution(data, catch=10, targets=None, exclusion=[]):
        lemmatizer = WordNetLemmatizer()
        transformation = []
        trash_words = stopwords.words('spanish')
        trash_words.append(['', ' '])
        trash_words.append(exclusion)
        for raw in data["text"]:
            tweet = norm.whitespace(remv.punctuation(raw))
            if (targets == None) or (True in [target in tweet for target in targets]):
                for word in tweet.split(" "):
                    transformation.append(lemmatizer.lemmatize(word))
        register = Counter(transformation)

        filtered = {}
        for k in register.keys():
            if k not in trash_words:
                filtered[k] = register[k]
        
        ordered = sorted(filtered.items(), key=lambda item: item[1], reverse=True)
        for items in ordered[:catch]:
            plt.bar(items[0], items[1], color="black", width=0.5)
        plt.xticks(rotation=90)
        plt.show()
        return dict(ordered[:10])

    
    @staticmethod
    def set_distribution():
        return

class TimeLapsePlot:

    @staticmethod
    def label_tracing(file, labels):
        data = pd.read_csv(file)
        min_date = dt.datetime.strptime(min(data["date"]), "%Y-%m-%d")
        max_date = dt.datetime.strptime(max(data["date"]), "%Y-%m-%d")
        dates = np.arange(min_date, max_date, dt.timedelta(days=1)).astype(dt.datetime)
        points = np.zeros((len(labels), len(dates)))

        for l in range(len(labels)):
            i = 0
            for date in dates:
                points[l,i] = data[pd.to_datetime(data["date"]) == date][labels[l]].sum()
                i += 1
            plt.step(dates, points[l,:])
            plt.legend(labels)
            plt.xticks(rotation = 90)
        plt.show()
        return 
    

class StatisticsPrinter:

    @staticmethod
    def label_summary():
        return

    @staticmethod
    def match_summary():
        return