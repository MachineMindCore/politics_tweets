import pandas as pd
from tqdm.notebook import tqdm

import torch
from transformers import pipeline

class SentimentSetAnalizer:
    
    MODEL_TAG = {
        "DANE": "Recognai/bert-base-spanish-wwm-cased-xnli",
        "roberta": "vicgalle/xlm-roberta-large-xnli-anli",
    }

    def __init__(self, tag, device):
        tqdm.pandas()
        torch.cuda.empty_cache()
        self.zero_shot_classifier = pipeline(
            "zero-shot-classification",
            model = self.MODEL_TAG[tag],
            device = device,
        )
        return
    
    # Methods
    # Single text analizer
    def expand_sentiment(self, data, col_target, labels):
        expansion = pd.DataFrame(columns=labels)
        for text in data[col_target]:
            values = self.eval_sentiment(text,labels)
            chip = pd.DataFrame(columns=values["labels"], data=[values["scores"]])
            expansion = pd.concat([expansion, chip], axis='rows')
        expansion.set_index(data.index, inplace=True)
        data = pd.concat([data, expansion], axis='columns')
        return data

    def eval_sentiment(self, text, zero_shot_labels):
        if type(text) == str:      
            classification = self.zero_shot_classifier(
                text, 
                candidate_labels = zero_shot_labels, 
                multi_label = False
            )
        else:
            classification = {
                "labels": zero_shot_labels,
                "scores": [0]*len(zero_shot_labels),
            }
        return classification

""" 
data = pd.read_csv('SUSDATOS.csv', index_col = 0).reset_index().dropna(subset = ['SUCOLUMNADEINTERES'])
dfs = []
for index in tqdm(np.arange(data.shape[0])): 

    try: 

        post_date = data.iloc[index]['post_time'] #Esto es opcional.
        text = data.iloc[index]['user_comment'] #Esta es su columna de análisis

        df = sentiment_topic_analysis(text,
                                      zero_shot_classifier,
                                      zero_shot_labels = ['ETIQUETA1',
                                                          'ETIQUETA2']) #Aqui van las etiquetas de descortesía.

        df['PostDate'] = post_date #De nuevo, opcional. Puede eliminarlo.

        dfs.append(df)

    except KeyboardInterrupt: 
        break

    except: 
        print("error in dataset or function")

        pass

post_sentiment = pd.concat(dfs).astype('float', errors = 'ignore')

post_sentiment['Max'] = post_sentiment[['ETIQUETA1',
                                        'ETIQUETA2']].idxmax(axis = 1) 
post_sentiment_discrimination = post_sentiment[post_sentiment['Max'] == 'ETIQUETA1'].sort_values('ETIQUETA1', ascending = False)
post_sentiment_representativity = post_sentiment[post_sentiment['Max'] == 'ETIQUETA1'].sort_values('ETIQUETA1', ascending = False)

"""
