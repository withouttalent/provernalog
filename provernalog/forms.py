from django import forms
from .models import Parcel, City, GroupAppraise, SubgroupAppraise, Support

class FindForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ('cadastral_number',)


class ParcelAggregateForm(forms.Form):
    group_appraise__group_id = forms.IntegerField(min_value=0, label="Номер группы")
    subgroup_appraise__subgroup_id = forms.IntegerField(min_value=0, label="Номер подгруппы")
    group_appraise__type = forms.CharField(max_length=5, label="Тип объекта")
    region = forms.ModelChoiceField(queryset=City.objects.all(), label="Город")


class SupportForm(forms.Form):
    cadastral_number = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={"type": "hidden",
                                                                                              "style": "display:none",
                                                                                              }))
    sender = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Фамилия Имя Отчество",
                                                                     "title": "Фамилия Имя Очество в родительном падеже",
                                                                     'class': 'order_input'}))
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Ваш номер телефона",
                                                                    'class': 'order_input'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"placeholder": "Ваш email",
                                                                     'class': 'order_input'}))

    def save(self):
        print(self.cleaned_data)
        support = Support.objects.create(**self.cleaned_data)
        return support


class WordForm(SupportForm):
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Адрес регистрации заявителя',
                                                                      'class': 'order_input',
                                                                      }))

class OrderForm(SupportForm):
    cadastral_number = forms.CharField(label='', widget=forms.TextInput(attrs=({'placeholder': 'Кадастровый номер',
                                                                                'class': 'order_input'})))
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Адрес',
                                                                      'class': 'order_input'}))
    inn = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Инн", 'class': 'order_input'}))
