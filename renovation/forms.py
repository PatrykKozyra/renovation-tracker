from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Field
from crispy_forms.bootstrap import FormActions
from .models import Purchase, PurchaseCategory, Room, RoomProgress, RoomProgressPhoto, WorkSession, ElectricalCircuit


class PurchaseForm(forms.ModelForm):
    """Form for adding/editing purchases with beautiful UI"""

    class Meta:
        model = Purchase
        fields = ['date', 'category', 'vendor', 'amount', 'description', 'notes', 'receipt_photo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3"><i class="bi bi-receipt"></i> {% trans "Szczegóły zakupu" %}</h4>'),
            Row(
                Column('date', css_class='form-group col-md-4 mb-3'),
                Column('category', css_class='form-group col-md-4 mb-3'),
                Column('amount', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('vendor', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('receipt_photo', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz zakup'), css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url \'purchases_list\' %}" class="btn btn-secondary btn-lg ms-2">{% trans "Anuluj" %}</a>'),
            )
        )


class RoomProgressForm(forms.ModelForm):
    """Form for adding room progress"""

    class Meta:
        model = RoomProgress
        fields = ['room', 'date', 'description', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3"><i class="bi bi-clipboard-check"></i> {% trans "Nowy wpis postępu" %}</h4>'),
            Row(
                Column('room', css_class='form-group col-md-6 mb-3'),
                Column('date', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-3'),
            ),
            HTML('''
                <div class="mb-3">
                    <label class="form-label"><i class="bi bi-images"></i> {% trans "Zdjęcia" %}</label>
                    <input type="file" name="photos" multiple accept="image/*" class="form-control" id="photoInput">
                    <small class="form-text text-muted">{% trans "Możesz wybrać wiele zdjęć naraz" %}</small>
                </div>
                <div id="photoPreview" class="row g-2 mb-3"></div>
            '''),
            FormActions(
                Submit('submit', _('Dodaj postęp'), css_class='btn btn-success btn-lg'),
                HTML('<a href="{% url \'progress_list\' %}" class="btn btn-secondary btn-lg ms-2">{% trans "Anuluj" %}</a>'),
            )
        )


class WorkSessionForm(forms.ModelForm):
    """Form for logging work sessions"""

    class Meta:
        model = WorkSession
        fields = ['date', 'start_time', 'end_time', 'notes', 'rooms_worked_on']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'rooms_worked_on': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3"><i class="bi bi-clock-history"></i> {% trans "Nowa sesja pracy" %}</h4>'),
            Row(
                Column('date', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6 mb-3'),
                Column('end_time', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-3'),
            ),
            HTML('<div class="mb-3"><label class="form-label">{% trans "Pomieszczenia" %}</label></div>'),
            Row(
                Column('rooms_worked_on', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz sesję'), css_class='btn btn-warning btn-lg'),
                HTML('<a href="{% url \'sessions_list\' %}" class="btn btn-secondary btn-lg ms-2">{% trans "Anuluj" %}</a>'),
            )
        )


class ElectricalCircuitForm(forms.ModelForm):
    """Form for documenting electrical circuits"""

    class Meta:
        model = ElectricalCircuit
        fields = ['circuit_name', 'breaker_number', 'room', 'connected_appliances', 'amperage', 'notes']
        widgets = {
            'connected_appliances': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3"><i class="bi bi-lightning-fill"></i> {% trans "Obwód elektryczny" %}</h4>'),
            Row(
                Column('circuit_name', css_class='form-group col-md-6 mb-3'),
                Column('breaker_number', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('room', css_class='form-group col-md-6 mb-3'),
                Column('amperage', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('connected_appliances', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz obwód'), css_class='btn btn-info btn-lg'),
                HTML('<a href="{% url \'dashboard\' %}" class="btn btn-secondary btn-lg ms-2">{% trans "Anuluj" %}</a>'),
            )
        )


class PurchaseFilterForm(forms.Form):
    """Filter form for purchases list"""

    category = forms.ModelChoiceField(
        queryset=PurchaseCategory.objects.all(),
        required=False,
        empty_label=_('Wszystkie kategorie'),
        label=_('Kategoria')
    )

    vendor = forms.CharField(
        required=False,
        label=_('Sklep'),
        widget=forms.TextInput(attrs={'placeholder': _('Wpisz nazwę sklepu...')})
    )

    date_from = forms.DateField(
        required=False,
        label=_('Data od'),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    date_to = forms.DateField(
        required=False,
        label=_('Data do'),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='col-md-3'),
                Column('vendor', css_class='col-md-3'),
                Column('date_from', css_class='col-md-2'),
                Column('date_to', css_class='col-md-2'),
                Column(
                    Submit('filter', _('Filtruj'), css_class='btn btn-primary'),
                    HTML('<a href="{% url \'purchases_list\' %}" class="btn btn-secondary ms-2">{% trans "Wyczyść" %}</a>'),
                    css_class='col-md-2 d-flex align-items-end'
                ),
            )
        )
