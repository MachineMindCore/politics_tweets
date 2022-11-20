from re import sub

def remove_url(text):
    return sub(r'http\S+', '', text)

def date_hours(date):
    return 8766*date.year + 730*date.month + 24*date.day 