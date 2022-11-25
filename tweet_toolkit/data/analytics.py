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
    def general_distribution(data, catch=10, reference="text", targets=None, exclusion=[]):
        register = FrecuencyPlot.extract_text(data, reference, targets=targets, exclusion=exclusion)
        register = dict(islice(register.items(), catch))
        for k in register.keys():
            plt.bar(k, register[k], color="black", width=0.5)
        plt.grid()
        plt.xticks(rotation=-90)
        plt.show()
        return register

    
    @staticmethod
    def group_distribution(data, groups, reference="text"):
        register = FrecuencyPlot.extract_text(data, reference)
        acummulation = dict(zip(groups.keys(), [0]*len(groups.keys())))
        for k in register.keys():
            for label in groups.keys():
                if k in groups[label]:
                    acummulation[label] += register[k]
        
        f, ax = plt.subplots()
        for k in acummulation.keys():
            ax.bar(k, acummulation[k], color="black", width=0.5)
        ax.set_xlim(-1,len(acummulation.keys()))
        plt.grid()
        plt.xticks(rotation=-90)
        plt.show()     
        return acummulation

    @staticmethod
    def extract_text(data, reference, clean=True, targets=None, exclusion=[]):
        lemmatizer = WordNetLemmatizer()
        transformation = []
        for raw in data[reference]:
            tweet = norm.whitespace(remv.punctuation(raw))
            if (targets == None) or (True in [target in tweet for target in targets]):
                for word in tweet.split(" "):
                    transformation.append(lemmatizer.lemmatize(word))
        register = Counter(transformation)
        
        if clean:
            trash_words = stopwords.words('spanish')
            trash_words.append(['', ' '])
            trash_words.append(exclusion)
            filtered = {}
            for k in register.keys():
                if k not in trash_words:
                    filtered[k] = register[k]
            filtered = dict(sorted(filtered.items(), key=lambda item: item[1], reverse=True))
            register = filtered
        return register

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