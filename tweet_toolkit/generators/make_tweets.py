import sys, os
sys.path.append(os.path.join(sys.path[0],'..','..'))

import pandas as pd
from config import guest
from tweet_toolkit.helpers.handle import remove_url
from tweet_toolkit.data.miners import TweetParser
from argparse import ArgumentParser

def make_arguments():
    parser = ArgumentParser(description="tweets data extractor")
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int, default=100)
    parser.add_argument('--full', nargs='?', const='')
    return parser.parse_args()

def make_filename(args: ArgumentParser):
    if args.full == None:
        filename = f"{args.target}_[{args.start}-{args.stop}].csv"
        print(f"settings: target: {args.target}, interval: [{args.start}, {args.stop}]")
    else:
        filename = f"{args.target}_full.csv"
        print(f"settings: target: {args.target}, full extraction")
    print(f"--> pointing to {filename}")
    return filename

def extract(loader, args):
    print(f"--> extracting from @{args.target}")
    if args.full == None:
        data = loader.get_by_number(args.target, start=args.start, stop=args.stop)
    else:
        data = loader.get_full(args.target)
    return data

def save(data, file):
    print(f"--> saving {file}")
    frame = pd.DataFrame({
        "id":   list(map(lambda t: t._json['id'], data)),
        "user": list(map(lambda t: t._json['user']['screen_name'], data)),
        "text": list(map(lambda t: remove_url(t._json['full_text']), data)),
        "date": list(map(lambda t: t._json['created_at'], data)),
    })
    frame["date"] = pd.to_datetime(frame["date"]).dt.strftime("%d-%m-%Y")
    frame.to_csv(f"data/raw/{file}",  index=False)
    return


if __name__ == "__main__":
    args = make_arguments()
    print(args)
    if args.full != None:
        print("yes")
    name = make_filename(args)
    
    loader = TweetParser(
        key = guest.API_KEY,
        secret_key = guest.API_SECRET_KEY,
        token = guest.ACCESS_TOKEN,
        secret_token = guest.ACCESS_TOKEN_SECRET,
    )

    data = extract(loader, args)
    save(data, name)

