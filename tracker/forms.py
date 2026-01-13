from django import forms
from .models import UserProfile

class SurveyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nickname", "selected_categories", "num_habits", "dashboard_style", "focus_preference", "work_style"]

        # Survey fields -> tells django how to render each field on the web page
        widgets = {
            "nickname": forms.TextInput(attrs={"placeholder":"Enter your nickname"}),
            "selected_categories": forms.CheckboxSelectMultiple(), # allows multiple selections
            "num_habits": forms.NumberInput(attrs={"min": 1, "max": 20}),
            "dashboard_style": forms.RadioSelect(),                # only allows one selection
            "focus_preference": forms.RadioSelect(),
            "work_style": forms.RadioSelect(),
        }
    