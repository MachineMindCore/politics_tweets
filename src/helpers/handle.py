from re import sub

def remove_url(text):
    return sub(r'http\S+', '', text)