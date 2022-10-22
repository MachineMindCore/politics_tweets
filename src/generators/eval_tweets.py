import sys
from os import listdir
from os.path import isfile, join
sys.path.append(join(sys.path[0],'..','..'))

from argparse import ArgumentParser
from src.models.sentiment import SentimentSetAnalizer
import pandas as pd

def make_arguments():
    parser = ArgumentParser(description="tweets evaluator")
    parser.add_argument('--file', type=str)
    parser.add_argument('--model', type=str, default="spanish_DANE")
    parser.add_argument('--device', type=str, default="cpu")    
    parser.add_argument('--labels', type=str, nargs='+', default=["descortes", "cortes", "neutral"])
    parser.add_argument('--group', type=str, default="processed")
    parser.add_argument('--all', nargs='?', const='')
    return parser.parse_args()

def load_data(path):
    data = pd.read_csv(path)
    try:
        data.rename(columns={'Unnamed: 0':'id'}, inplace=True)
    except:
        pass
    return data

def eval_data(data, args, file):
    print(f"--> Evaluating {file}")
    analizer = SentimentSetAnalizer(tag=args.model, device=args.device)
    return analizer.expand_sentiment(data, col_target="text", labels=args.labels)

def save_data(data, file):
    print(f"--> saving {file}")
    data.to_csv(f"data/evaluated/{file}")

if __name__ == "__main__":
    args = make_arguments()
    if args.all == None:
        print(args.file)
        path = f"data/{args.group}/{args.file}"
        data = load_data(path)
        evaluated = eval_data(data, args, args.file)
        save_data(evaluated, args.file)
    else:
        files = [f for f in listdir(f"data/{args.group}") if isfile(join(f"data/{args.group}", f))]
        for file in files:
            path = f"data/{args.group}/{file}"
            print(path)
            data = load_data(path)
            evaluated = eval_data(data, args, file)
            save_data(evaluated, file)