from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Button
from crispy_forms.bootstrap import FormActions

from .models import Ballot

from jsonschema import validate, ValidationError
import json


ballotschema = {
    "type": "array",
    "items": {
        "type": "integer"
    },
    "minItems": 1,
    "uniqueItems": True
}


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

    def clean_data(self):
        data = self.cleaned_data['data']
        try:
            obj = json.loads(data)
            validate(obj, ballotschema)
        except ValueError:
            raise forms.ValidationError("Could not decode JSON from data")
        except ValidationError:
            raise forms.ValidationError("Bad data.")

        return data
