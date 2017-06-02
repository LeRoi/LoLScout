# query.py
# Make queries and handle errors to Riot API

import json
import time
import urllib
from query_exceptions import *

def get_api_key(src="data/api_key.txt"):
    api_file = open(src, 'r')
    lines = [line.strip() for line in api_file.readlines()]
    return lines[0]

def query_riot_api(query):
    """Returns JSON from querying Riot API.

    Throws API errors with well-formatted JSON."""
    web_data = urllib.urlopen(query)
    raw_data = [line.strip() for line in web_data.readlines()]
    try:
        json_data = json.loads(raw_data[0])
    except ValueError:
        print json_data
        raise_exception(404)

    if 'status' in json_data.keys():
        if 'status_code' not in json_data['status'].keys():
            raise Exception("Poorly formatted data returned on query: " + str(query))
        else:
            raise_exception(json_data['status']['status_code'])

    return json_data

def query_with_retries(query, retries=3):
    """Query Riot API and retry on error 429.

    After [[retries]] attempts, returns an empty map."""
    response = {}
    for i in range(retries):
        try:
            response = query_riot_api(query)
            break
        except q429Exception:
            print "\tRate limit exceeded, waiting 10 seconds..."
            time.sleep(10)
    return response

def response_at(query, response, key):
    """Returns the value associated with key, if it exists.

    Throws generic exception if key does not exist."""
    if key not in response.keys():
        raise Exception("Incorrect data returned for key %s.\nQuery:\n%s\nResponse:\n%s" % (key, query, response))
    return response[key]

summoner_name_query = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/%s?api_key=%s"
def get_summoner_id(summoner_name, api_key):
    """Returns the ID associated with the summoner name provided.

    Throws 400, 401, 404, 429, 501, 503, and generic exceptions."""

    query_name = summoner_name.replace(" ", "%20").lower()
    response_name = summoner_name.replace(" ", "").lower()
    query = summoner_name_query % (query_name, api_key)
    summoner_id = query_with_retries(query)
    return response_at(query, summoner_id, "id")

# Distinct from summoner account id query
summoner_id_query = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/%s?api_key=%s"
def get_summoner_names(summoner_ids, api_key):
    """Returns the name associated with the provided ID.

    Throws 400, 401, 404, 429, 501, 503, and generic exceptions."""

    names = []
    if len(summoner_ids) == 0:
        return names

    for summoner_id in summoner_ids:
        query = summoner_id_query % (summoner_id, api_key)
        summoner_name = query_with_retries(query)
        names.append(response_at(query, summoner_name, "name").title())
    return names

match_query = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/%s/recent?api_key=%s"
def get_recent_matches(summoner_name, api_key):
    """Returns JSON array of match data."""
    summoner_id = get_summoner_id(summoner_name, api_key)
    query = match_query % (summoner_id, api_key)
    match_history = query_with_retries(query)
    return response_at(query, match_history, "games")

item_query = "https://na1.api.riotgames.com/lol/static-data/v3/items?api_key=%s"
def get_item_data(api_key):
    return query_riot_api(item_query % api_key)

champion_query = "https://na1.api.riotgames.com/lol/static-data/v3/champions?api_key=%s"
def get_champion_data(api_key):
    return query_riot_api(champion_query % api_key)

spell_query = "https://na1.api.riotgames.com/lol/static-data/v3/summoner-spells?api_key=%s"
def get_summoner_spell_data(api_key):
    return query_riot_api(spell_query % api_key)
