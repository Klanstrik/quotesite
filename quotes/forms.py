# quotes/forms.py
from django import forms
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    # чтобы источники подгружались
    source = forms.ModelChoiceField(
        queryset=Source.objects.all(),
        empty_label="— выберите источник —",
        label="Источник",
    )

    class Meta:
        model = Quote
        fields = ["source", "text", "author", "weight", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # порядок источников
        self.fields["source"].queryset = Source.objects.order_by("name")

        # базовые тёмные стили для остальных полей
        dark = (
            "w-full rounded-xl bg-white/5 border border-white/10 "
            "px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        )
        self.fields["text"].widget = forms.Textarea(attrs={"rows": 4, "class": dark})
        self.fields["author"].widget = forms.TextInput(attrs={"class": dark})
        self.fields["weight"].widget = forms.NumberInput(attrs={"class": dark})
        self.fields["is_active"].widget = forms.CheckboxInput(
            attrs={"class": "h-4 w-4 text-indigo-600 border-gray-300 rounded"}
        )


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dark = (
            "w-full rounded-xl bg-white/5 border border-white/10 "
            "px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        )
        self.fields["name"].widget = forms.TextInput(attrs={"class": dark})
