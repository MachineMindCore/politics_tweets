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
        register = FrecuencyHandle.extract_tokens(data, reference, targets=targets, exclusion=exclusion)
        register = dict(islice(register.items(), catch))
        for k in register.keys():
            plt.bar(k, register[k], color="black", width=0.5)
        plt.grid()
        plt.xticks(rotation=-90)
        plt.show()
        return register

    
    @staticmethod
    def group_distribution(data, groups, reference="text"):
        register = FrecuencyHandle.extract_tokens(data, reference)
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
    def group_evaluation(data, groups, labels, reference="text"):            
        register = FrecuencyHandle.extract_tokens_with_index(data, reference)
        acummulation = {key: dict(zip(labels, [0]*len(labels))) for key in groups.keys()}

        for key in register.keys():
            for g_key in groups.keys():
                if key in groups[g_key]:
                    for index in register[key][1]:
                        category, _ = FrecuencyHandle.eval_classification(data[labels], index)
                        if category != None:
                            acummulation[key][category] += 1

        width = 0.1  # the width of the bars
        x = np.arange(len(groups.keys()))*(1.5*width*len(groups.keys())) # the label locations
        fig, ax = plt.subplots()
        ax.grid(axis="y")
        i = 0
        for label in labels:
            values = [acummulation[k][label] for k in acummulation.keys()]
            ax.bar(x - width*i, values, width, label=label)
            if i>0:
                i = -i
            else:
                i = -i+1
        ax.set_xticks(x)
        ax.set_xticklabels(groups.keys())
        ax.legend()
        plt.show()
        return acummulation
    
    @staticmethod
    def group_correlation(data):
        return

class FrecuencyHandle:
    
    @staticmethod
    def extract_tokens(data, reference, clean=True, targets=None, exclusion=[]):
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
            for ex in exclusion: trash_words.append(ex) 
            filtered = {}
            for k in register.keys():
                if k not in trash_words:
                    filtered[k] = register[k]
            filtered = dict(sorted(filtered.items(), key=lambda item: item[1], reverse=True))
            register = filtered
        return register
    
    @staticmethod
    def extract_tokens_with_index(data, reference, clean=True, targets=None, exclusion=[]):
        lemmatizer = WordNetLemmatizer()
        transformation = []
        i = 0
        for raw in data[reference]:
            tweet = norm.whitespace(remv.punctuation(raw))
            if (targets == None) or (True in [target in tweet for target in targets]):
                for word in tweet.split(" "):
                    transformation.append((lemmatizer.lemmatize(word), i))
            i += 1

        register = {}
        for word_container in transformation:
            if not word_container[0] in register.keys():
                register[word_container[0]] = [0, []]
            register[word_container[0]] = [register[word_container[0]][0]+1, register[word_container[0]][1]+[word_container[1]]] 
        
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
    

    @staticmethod
    def eval_classification(scores, idx, margin=0.6):
        if len(scores.columns)==1 and scores.iloc[0,0]>margin:
            return list(scores.columns)[0], scores.iloc[0,0]
        
        primary = {"label":None, "val":0}
        secundary = {"label":None, "val":0}
        for label in scores.columns:
            if scores[label].iloc[idx]>primary["val"]:
                secundary = primary
                primary = {"label": label, "val": scores[label].iloc[idx]}
        if secundary["val"]*(margin+1) < primary["val"]:
            return primary["label"], primary["val"]
        else: 
            return None, None


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