"""
	Assigns users to slots and gets right rules (in DB), each game
		-2di-iii, below
		-imports signals from metagamesignals.py, to assign logged-in users to slots
		-determines right rules to use by querying DB by game number, then imports those
			rules from gamerules/(rule_set)
		-controls logic to launch game and update turns (according to given rule_set)
		-updating turns also involves logging actions in the action_log
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from game.gamemetamethods import login_user, logout_user




"""
Supposed to assign users to game slots when they log in - doesn't seem to work yet
Remove users from game slots when they log out
"""
  
#user_logged_in.connect(login_user)
#user_logged_out.connect(logout_user)

# Another attempt to create a list of logged in users, to create game

# http://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users

# Best: When successfully logged in, 1) go to /lobby/ instead of /game/; 2) click on link
# that redirects to /waitroom/ and adds you as a new record to wait_room table;
# 3) have /waitroom/ display all members of the wait_room, per link above; and finally
# 4) have link in /waitroom/ that allows (at first) any member of wait room to join
# game, where /game/ correctly slots players into farms, and locks player list once first
# player joins

"""
So:

1) Use logged_user table for now, for waitroom members - okay
2) Create lobby app, with views and urlconfs for /lobby/ and /waitroom/ - done
3) With waitroom view, call the function that will add user to logged_user table - done
4) Add link in /waitroom/ to /game/ - done (NOW NEED TO REMOVE USERS FROM LOGGED_USER
	TABLE WHEN THEY LEAVE THE WAITROOM!)
5) Have game render with users as context
6) When first human enters game, create player objects in InitState
7) At some point, move logged_user table to lobby.models, not game.models
"""