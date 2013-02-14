from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import Ballot
from .validators import validate_ballot


class BallotForm(forms.ModelForm):
    class Meta:
        model = Ballot
        fields = ('data', )
        widgets = {
            'data': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('data'),
            FormActions(
                Submit('submit', 'Submit'),
                Button('cancel', 'Cancel', onclick='window.location="/"')
            )
        )
        super(BallotForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(BallotForm, self).clean()
        data = cleaned_data['data']
        validate_ballot(data)
        return cleaned_data
