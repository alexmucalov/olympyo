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

class OperatedObjectActionForm(forms.Form):
    set_wage_1 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_2 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    sell = forms.BooleanField(required=False)
    set_min_bid = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    #on dynamic init, create set_wage_i, where i is created for as many set_wage actions
    #available on that farm, based on labour_spots!
  
    #FORM LEVEL
    #If a player is able to work farms, then a
    #player may only work one farm each turn... (later)
    
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

    def clean_sell(self):
        data = self.cleaned_data['sell']
        if data == True:
            data = 'yes'
        return data

class OtherObjectActionForm(forms.Form):
    bid_to_buy = forms.DecimalField(max_digits=5, decimal_places=2) # This is a required field
    
    def clean_bid_to_buy(self):
        data = self.cleaned_data['bid_to_buy']
        if data:
            if data <= 0:
                raise forms.ValidationError("You've got to bid something")
        return data


class SelfObjectActionForm(forms.Form):
    work = forms.BooleanField() # This is a required field
    
    
    def clean_work(self):
        data = self.cleaned_data['work']
        if data == True:
            data = 'yes'
        elif data == False:
            data = 'no'
        return data


class DevelopingObjectActionForm(forms.Form):
    set_wage_1 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_2 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_3 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_4 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    sell = forms.BooleanField(required=False)
    set_min_bid = forms.DecimalField(max_digits=5, decimal_places=2, required=False)

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

    def clean_set_wage_3(self):
        #Set_wages must be > 0
        data = self.cleaned_data['set_wage_3']
        if data:
            if data <= 0:
                raise forms.ValidationError("You've got to offer something")
        return data
    
    def clean_set_wage_4(self):
        #Set_wages must be > 0
        data = self.cleaned_data['set_wage_4']
        if data:
            if data <= 0:
                raise forms.ValidationError("You've got to offer something")
        return data

    def clean_sell(self):
        data = self.cleaned_data['sell']
        if data == True:
            data = 'yes'
        return data


class SellObjectActionForm(forms.Form):
    set_min_bid = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    take_off_market = forms.BooleanField(required=False)
    
    def clean_take_off_market(self):
        data = self.cleaned_data['take_off_market']
        if data == True:
            data = 'yes'
        return data


class BuyObjectActionForm(forms.Form):
    bid_to_buy = forms.DecimalField(max_digits=5, decimal_places=2) # This is a required field
    
    def clean_bid_to_buy(self):
        data = self.cleaned_data['bid_to_buy']
        if data:
            if data <= 0:
                raise forms.ValidationError("You've got to bid something")
        return data