import sys, os
sys.path.append(os.path.join(sys.path[0],'..'))

import pandas as pd
from config import guest
from src.data.miners import TweetParser
from argparse import ArgumentParser

def make_arguments():
    parser = ArgumentParser(description="tweets data extractor")
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int, default=100)
    return parser.parse_args()

def make_filename(args: ArgumentParser):
    filename = f"{args.target}_({args.start}-{args.stop}).csv"
    return filename

def extract(loader, args):
    data = loader.get_by_number(args.target, start=args.start, stop=args.stop)
    return data

def save(data, file):
    frame = pd.DataFrame({
        "user": list(map(lambda t: t._json['user']['screen_name'], data)),
        "text": list(map(lambda t: t._json['full_text'], data)),
        "date": list(map(lambda t: t._json['created_at'], data)),
    })
    frame.to_csv(f"data/raw/{file}")
    return


if __name__ == "__main__":
    args = make_arguments()
    name = make_filename(args)
    
    loader = TweetParser(
        key = guest.API_KEY,
        secret_key = guest.API_SECRET_KEY,
        token = guest.ACCESS_TOKEN,
        secret_token = guest.ACCESS_TOKEN_SECRET,
    )

    data = extract(loader, args)
    save(data, name)

