
"""     parser.add_argument('--date', type=str, nargs='+', default=[], required=False)
    parser.add_argument('--match', type=str, nargs='+', default=[], required=False)
    return parser.parse_args()

def make_filename(args: ArgumentParser):
    def rewrite(obj: list):
        text = ''
        for item in obj:
            text += f"{item}-"
        return text[:-1]

    filename = args.target
    if args.match != []:
        filename += f"_[{rewrite(args.match)}]"
    if args.date != []:
        filename += f"_({args.date[0]}|{args.date[1]})"
    filename += ".csv"
    return filename

def extract(loader, args):
    data = loader.get_full()
    if args.match != []:
        pass


if __name__ == "__main__":
    args = make_arguments()
    name = make_filename(args)
    loader = TweetParser(
        key = guest.API_KEY,
        secret_key = guest.API_SECRET_KEY,
        token = guest.ACCESS_TOKEN,
        secret_token = guest.ACCESS_TOKEN_SECRET,
    )
     """
import sys, os
from tokenize import group
sys.path.append(os.path.join(sys.path[0],'..'))

import pandas as pd
from config import guest
from src.data.miners import TweetParser
from argparse import ArgumentParser
from datetime import datetime as dt

def make_arguments():
    parser = ArgumentParser(description="tweets filter pipeline")
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--match', type=str, nargs='+', default=[])
    parser.add_argument('--date', type=str, nargs='+', default=[])
    parser.add_argument('--group', type=str, default="raw")
    return parser.parse_args()

def load_file(file: str, group = "raw"):
    return pd.read_csv(f"data/{group}/{file}", index_col=0)

def make_filename(args: ArgumentParser):
    def rewrite(obj: list):
        text = ''
        for item in obj:
            text += f"{item}-"
        return text[:-1]
    
    filename = f"{args.file}".split('_')[0]
    if "full" in args.file:
        filename += "_full"
    if args.match != []:
        filename += f"_[{rewrite(args.match)}]"
    if args.date != []:
        filename += f"_[{args.date[0]}&{args.date[1]}]"
    filename += ".csv"
    print(f"transformer: match == {args.match}, date == {args.date}")
    print(f"--> pointing to {filename}")
    return filename

def filter_data(data: pd.DataFrame, args):
    print("--> filtering match & dates")
    if args.match != []:
        data['match'] = data['text'].str.findall('(' + '|'.join(args.match) + ')')
        data = data[data['match'].astype(bool)]
    #Wed Oct 19 18:38:45 +0000 2022
    #%a %b %d %H:%M:%S %z %Y
    if args.date != []:
        data['date'] = pd.to_datetime(data['date'])
        data = data[(data['date'] > args.date[0]) & (data['date'] < args.date[1])]
    return data

def save(data, file):
    print(f"--> saving {file}")
    data.to_csv(f"data/processed/{file}")
    return


if __name__ == "__main__":
    args = make_arguments()
    data = load_file(args.file, group=args.group)
    name = make_filename(args)
    new_data = filter_data(data, args)
    save(new_data, name)

