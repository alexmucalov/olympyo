"""
* File must be named after game_ruleset that applies
* For game.views to be able to import ActionForm properly
"""


from django import forms

class ActionForm(forms.Form):
    set_wage_1 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_2 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    work = forms.CharField(required=False)
    
    #on dynamic init, create set_wage_i, where i is created for as many set_wage actions
    #available on that farm, based on labour_spots!