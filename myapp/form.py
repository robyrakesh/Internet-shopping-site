from django import forms
from myapp.models import Order, Client


Client_list = Client.objects.all()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Client', 'Product', 'num_units']
        widgets = {'Client': forms.Select(choices= Client_list)}
        labels = {'num_units': u'Quantity', 'Client': u'ClientName'}


class InterestForm(forms.Form):
    interested = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int, choices=((1, "Yes"), (0, "No")))
    quantity = forms.IntegerField(initial=1, min_value=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)


class RegisterForm(forms.Form):
    register = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=bool,
                                      choices=((True, "Yes"), (False, "No")), label='Do you want to become a client?')
