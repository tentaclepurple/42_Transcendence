from statistic.models import Statistic

def update_elo_points(winner: Statistic, loser: Statistic):    
    expected_score_winner = expected_score(winner.elo, loser.elo)
    expected_score_loser = expected_score(loser.elo, winner.elo)

    winner.elo = int(calculate_elo(winner.elo, expected_score_winner, True))
    loser.elo =  int(calculate_elo(loser.elo, expected_score_loser, False))

    winner.games_played += 1
    loser.games_played += 1

    winner.games_won += 1

    winner.save()
    loser.save()

def expected_score(userA_elo, userB_elo):
    return 1 / (1 + 10 ** ((userB_elo - userA_elo) / 400))

def calculate_elo(winner_elo, expected_score, win):
    k = 40
    if win:
        new_elo = winner_elo + k * (1 - expected_score)
    else:
        new_elo = winner_elo + k * (0 - expected_score)
    if new_elo < 0:
        new_elo = 0
    return new_elo
