"""
specifies turn update logic for version 1 rules
		-2div-v, below
		-imports from gameforms.py for specific actions' forms (useful for validating)
		-defines the game functions that each view function will call when a given button 
			is pressed
		-(When you POST, you post to the same urlconf, which calls a view function, which 
			can in turn call any other function you want - but you want to keep views and
			game logic separate! Want refreshed pages to query all players' updated info?
			Or keep all hidden? Or keep all other players' info hidden? Not difficult, no
			matter what.)
			-- Push public/private wage display, e.g., back to game rules, and leave as 
				an argument in game rules' functions
			-- Leave as arguments, for game rules to read, things like player_wage_info
				(public or private), farm_productivity_parameter (squared, cubed, etc.)
			-- Put these parameters in the DB attached to each game, under something like
				a rule_parameters column and a rule_values column, and have the game 
				rules query those parameters and store those values locally when a 
				game_init function is called
		-So:
			-- On a turn, gamerules house the DB query functions that views will call
			-- When turns update - called by gamecontroller - gamerules will update state,
				per 2dv. below; and then gamecontroller (?) will log all changes
"""