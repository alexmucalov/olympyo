"""
* File must be named after game_ruleset that applies
* for game.views to be able to import ActionForm properly
"""


from django import forms

class ActionForm(forms.Form):
    work = forms.CharField() # This is a required field
    set_wage_1 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_2 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    #on dynamic init, create set_wage_i, where i is created for as many set_wage actions
    #available on that farm, based on labour_spots!
    
    #ADD CUSTOM FORM VALIDATION!!
        #If a player works a farm, then must set one fewer wage than they have labour_spots
        #If a player does not work a farm, then a player must set as many as labour_spots
        #A player may only work one farm each turn