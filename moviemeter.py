from imdb import IMDb
from functools import lru_cache
import json
import datetime
from flask import Flask, jsonify, request

now = datetime.datetime.now()

moviemeter = Flask(__name__)

ia = IMDb()

def get_top(dataset):
    if dataset == "popular100_movies":
        return ia.get_popular100_movies(), 'popular movies 100 rank'
    if dataset == "popular100_tv":
        return ia.get_popular100_tv(), 'popular tv 100 rank'
    if dataset == "top250_tv":
        return ia.get_top250_tv(), 'top tv 250 rank'
    if dataset == "top250_movies":
        return ia.get_top250_movies(), 'top 250 rank'
    if dataset == "top250_indian_movies":
        return ia.get_top250_indian_movies(), 'top indian 250 rank'

def list_normalize(list, rank):
    table = []
    for item in list:
        table.append(
            {'title': item.data['title'],
            'imdb_id': 'tt' + item.getID(),
            'rating': item.data['rating'],
            'year': item.data['year'],
            'votes': item.data['votes'],
            'rank': item.data[rank]}
        )
    return table

def list_json(list, rank):
    return json.dumps(list_normalize(list, rank))

def filter_list(dataset, rating=0, year=0, votes=0, max=250, fresh=False):
    top, rank = get_top(dataset)
    result = []
    if fresh:
        year = (now.year - 1)
    for item in top:
        try:
            if (item.data['rating'] >= rating) and (item.data['year'] >= year) and (item.data['votes'] >= votes):
                result.append(item)
        except:
            # some items don't have years this will skip those weird ones
            pass
    return result[:max], rank

@moviemeter.route('/moviemeter/<dataset>', methods = ['GET'])
def api_handler(dataset):
    try:
        reqRating=int(request.args.get('rating'))
    except:
        reqRating=0

    try:
        reqYear=int(request.args.get('year'))
    except:
        reqYear=0

    try:
        reqVotes=int(request.args.get('votes'))
    except:
        reqVotes=0

    try:
        reqMax=int(request.args.get('max'))
    except:
        reqMax=250

    try:
        reqFresh=request.args.get('fresh')
    except:
        reqFresh=False

    # get the result with filters applied
    resultList, rank = filter_list(dataset=dataset, rating=reqRating,year=reqYear,votes=reqVotes,max=reqMax,fresh=reqFresh)

    # log requested query
    print(json.dumps({
        'rating': reqRating,
        'year': reqYear,
        'votes': reqVotes,
        'max': reqMax,
        'fresh': reqFresh
    }))

    # return json
    return list_json(resultList, rank)

if __name__ == "__main__":
    port = 6543
    moviemeter.run(host='0.0.0.0', port=port)
