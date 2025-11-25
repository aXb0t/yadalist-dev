from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    """UserCreationForm with design-system CSS classes applied to widgets."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-input").strip()
            # Avoid browser autofill styling conflicts
            field.widget.attrs.setdefault("autocomplete", "off")


class LoginForm(AuthenticationForm):
    """AuthenticationForm with design-system CSS classes applied."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-input").strip()
            field.widget.attrs.setdefault("autocomplete", "off")
