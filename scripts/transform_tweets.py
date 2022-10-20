
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