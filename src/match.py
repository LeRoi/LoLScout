# match.py
# Parse match JSON data

def get_bans(match):
    """Return a nested list of [blue bans, red bans]."""
    bans = [[], []]
    teams = match["teams"]
    for i in range(len(teams)):
        game_bans = teams[i]["bans"]
        for ban in game_bans:
            bans[i].append(str(ban["championId"]))
    return bans