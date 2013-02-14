from django import forms

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
