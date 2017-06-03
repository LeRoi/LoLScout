# main.py
# Main console

import match, query

def main():
    key = query.get_api_key()
    champion_data = query.get_champion_data(key)
    last_match = query.get_latest_match("Excerpt", key)
    bans = match.get_bans(last_match)
    for team in bans:
        print "Team:"
        for ban in team:
            print "\t%s" % (champion_data[ban]["name"])
        

if __name__ == "__main__":
    main()