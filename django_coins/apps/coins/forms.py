from apps.core.models import User
from django.forms import ModelForm, inlineformset_factory

from apps.core.models import Filter


class PatternForm(ModelForm):
    class Meta:
        model = Filter
        exclude = ()


PatternFormSet = inlineformset_factory(
    User, Filter, form=PatternForm, extra=1
)