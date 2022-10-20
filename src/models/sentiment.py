import json
import numpy as np
import pandas as pd
from dateparser import parse
from tqdm.notebook import tqdm

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, BertTokenizerFast

tqdm.pandas()
torch.cuda.empty_cache()

# Cargue el modelo zero shot en español 
 
zero_shot_classifier = pipeline("zero-shot-classification", model = "Recognai/bert-base-spanish-wwm-cased-xnli", device = "cpu")

# Aquí puede cargar el modelo multilingue. Los modelos arrojan resultados diferentes. Revise cuál le resulta más útil. 

#zero_shot_classifier = pipeline("zero-shot-classification", model = "vicgalle/xlm-roberta-large-xnli-anli",
#                                  device = 0)

def sentiment_topic_analysis(text, zero_shot_classifier, zero_shot_labels): 

    if type(text) == str:
                
        topic = zero_shot_classifier(text, candidate_labels = zero_shot_labels, multi_label = False) 
        
        topic_df = pd.DataFrame([topic['scores']], columns = topic['labels'])
              
        topic_df['text'] = text
        
        return topic_df
        
    else:
        
        return None

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