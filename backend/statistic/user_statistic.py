import os
import sys
import django
import django.apps
import argparse

sys.path.append('/app/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
if not django.apps.registry.apps.ready:
    django.setup()

from users.models import CustomUser as User
from statistic.models import Statistic

def update_elo_points(winner, loser):
	try:
		user_winner = User.objects.get(username=winner)
		user_loser = User.objects.get(username=loser)
	except User.DoesNotExist:
		print("User does not exist")
		return
	
	winner_statistic = user_winner.statistics
	loser_statistic = user_loser.statistics

	expected_score_winner = expected_score(winner_statistic.elo, loser_statistic.elo)
	expected_score_loser = expected_score(loser_statistic.elo, winner_statistic.elo)

	winner_statistic.elo = calculate_elo(winner_statistic.elo, expected_score_winner, True)
	loser_statistic.elo =  calculate_elo(loser_statistic.elo, expected_score_loser, False)

	winner_statistic.games_played += 1
	loser_statistic.games_played += 1

	winner_statistic.games_won += 1

	winner_statistic.save()
	loser_statistic.save()

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

def main():
	parser = argparse.ArgumentParser(description='Update ELO points for two users')
	parser.add_argument('-w', '--winner', type=str, help='winner User')
	parser.add_argument('-l', '--loser', type=str, help='loser User')

	args = parser.parse_args()

	if args.winner and args.loser:
		update_elo_points(args.winner, args.loser)

if __name__ == '__main__':
	main()