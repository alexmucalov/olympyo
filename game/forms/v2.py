"""
* File must be named after game_ruleset that applies
* for game.views to be able to import ActionForm properly
* This file is game-specific! Each game's single ActionForm
* will hold all the post logic for any action available in that game
* For example, farm_village could have set_wage_actions and work
* on farm objects that one owns, and it could have a buy action on objects
* that one doesn't own - and all those actions would be in the same form:
* The uncorresponding fields can be told to hide, from logic placed here in forms.py
* In this way, all actions will be in one form, but only the correct actions will
* display in the game view
"""


from django import forms

class OwnObjectActionForm(forms.Form):
    set_wage_1 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_2 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    #on dynamic init, create set_wage_i, where i is created for as many set_wage actions
    #available on that farm, based on labour_spots!
  
    #FORM LEVEL
    #If a player is able to work farms, then a
    #player may only work one farm each turn... (later)
    
    def clean_work(self):
        data = self.cleaned_data['work']
        if data.lower() == 'yes' or data.lower() == 'no':
            data = data.lower()
        else:
            raise forms.ValidationError("Work must be yes or no.")
        return data
    
    def clean_set_wage_1(self):
        #Set_wages must be > 0
        data = self.cleaned_data['set_wage_1']
        if data:
            if data <= 0:
                raise forms.ValidationError("You've got to offer something")
        return data
    
    def clean_set_wage_2(self):
        #Set_wages must be > 0
        data = self.cleaned_data['set_wage_2']
        if data:
            if data <= 0:
                raise forms.ValidationError("You've got to offer something")
        return data
    
    def clean(self):
        cleaned_data = super(ActionForm, self).clean()
        work = cleaned_data.get('work')
        set_wage_1 = cleaned_data.get('set_wage_1')
        set_wage_2 = cleaned_data.get('set_wage_2')

        if work == 'yes':
            # If a player works a farm, then must set one 
            # fewer wage than player has labour_spots
            if set_wage_1 and set_wage_2:
                raise forms.ValidationError("You can't hire for more "
                        "spots than you have available.")
            elif not set_wage_1 and not set_wage_2:
                raise forms.ValidationError("You've got room to hire "
                        "one more labourer.")

        if work == 'no':
            # If a player does not work a farm, then 
            # a player must set as many as labour_spots
            if not set_wage_1 or not set_wage_2:
                raise forms.ValidationError("You've got room to hire "
                        "two labourers.")

        return cleaned_data


class OtherObjectActionForm(forms.Form):
    buy = forms.CharField() # This is a required field
    
    def clean_buy(self):
        data = self.cleaned_data['buy']
        if data.lower() == 'yes':
            data = data.lower()
        else:
            raise forms.ValidationError("If you're going to buy, buy must be 'yes'!")
        return data