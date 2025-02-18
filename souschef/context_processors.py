import datetime

def date(request):
    today = datetime.datetime.today().date()
    date = datetime.datetime.strftime(today, '%a %d %b %Y')
    return {'date': date}