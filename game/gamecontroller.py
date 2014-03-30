"""
	Assigns users to slots and gets right rules (in DB), each game
		-2di-iii, below
		-imports signals from metagamesignals.py, to assign logged-in users to slots
		-determines right rules to use by querying DB by game number, then imports those
			rules from gamerules/(rule_set)
		-controls logic to launch game and update turns (according to given rule_set)
		-updating turns also involves logging actions in the action_log
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out
from game.gamemetamethods import login_user, logout_user

"""
Assign users to game slots when they log in;
Remove users from game slots when they log out
"""
  
user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)