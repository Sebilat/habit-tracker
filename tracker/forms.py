from django import forms
from .models import UserProfile, CATEGORY_CHOICES

class SurveyForm(forms.ModelForm):
    selected_categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = UserProfile
        fields = ["nickname", "selected_categories", "num_habits", "dashboard_style", "focus_preference", "work_style"]

        # Survey fields -> tells django how to render each field on the web page
        widgets = {
            "nickname": forms.TextInput(attrs={"placeholder":"Enter your nickname"}),
            "num_habits": forms.NumberInput(attrs={"min": 1, "max": 20}),
            "dashboard_style": forms.RadioSelect(),                # only allows one selection
            "focus_preference": forms.RadioSelect(),
            "work_style": forms.RadioSelect(),
        }
    