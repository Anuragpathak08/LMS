from django import forms
from .models import LeaveRequest
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class LeaveRequestForm(forms.ModelForm):

    class Meta:
        model = LeaveRequest
        fields = ["start_date","end_date","reason"]

        widgets = {
            "start_date": forms.DateInput(attrs={"type":"date"}),
            "end_date": forms.DateInput(attrs={"type":"date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date > end_date:
            raise forms.ValidationError("End date must be after start date")

        '''
        department = self.user.department
        conflict = LeaveRequest.objects.filter(
            user__department=department,
            status="approved"
        ).filter(
            Q(start_date__lte=end_date) &
            Q(end_date__gte=start_date)
        )

        if conflict.exists():
            raise forms.ValidationError(
                "Another employee from your department is already on leave during this period."
            )'''

        return cleaned_data
