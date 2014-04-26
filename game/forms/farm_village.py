from django import forms

class OwnedFarmActionForm(forms.Form):
    set_wage_1 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    set_wage_2 = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    work = forms.CharField(required=False)
    
    #on dynamic init, create set_wage_i, where i is created fro as many set_wage actions
    #available on that farm, based on labour_spots!