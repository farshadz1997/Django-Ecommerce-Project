from django import forms
from django.db.models import Case, OuterRef, Q, Value, When
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Voucher


class VoucherForm(forms.Form):
    voucher_code = forms.CharField(label=_('Promo Code:'), 
                                   max_length=10, 
                                   required=True, 
                                   widget=forms.TextInput(attrs={'class': 'input-text', 'placeholder':'promotion code', 'id': 'voucher_code', 'type': 'text'})
                                   )
    
    def __init__(self, user=None, *args, **kwargs):
        super(VoucherForm, self).__init__(*args, **kwargs)
        self.user_id = user
    
    def clean(self):
        cd = super(VoucherForm, self).clean()
        code = cd.get('voucher_code')
        voucher = Voucher.objects.filter(Q(max_use__gt=0) | Q(max_use=None),
                                        voucher_code__exact=code,
                                        is_active=True, 
                                        valid_from__lte=timezone.now(), 
                                        valid_until__gte=timezone.now())
        if voucher.exists():
            used_by_user = voucher.annotate(eligible=Case(
                When(one_time_use=True, then=Value(not voucher.filter(users=self.user_id).exists())),
                When(one_time_use=False, then=Value(True)),
                default=Value(True)
                )).values('eligible')
            if used_by_user.first()['eligible']:
                return cd
            else:
                raise forms.ValidationError(_('You already used this promo code.'))
        else:
            raise forms.ValidationError(_('Promo code is invalid'))