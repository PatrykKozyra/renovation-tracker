from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Field
from crispy_forms.bootstrap import FormActions
from .models import Purchase, PurchaseCategory, Room, RoomProgress, RoomProgressPhoto, WorkSession, ElectricalCircuit, Property, DropdownChoice, Equipment, EquipmentPhoto, EquipmentAssignment, RenovationTask, ShoppingItem


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
        current_property = kwargs.pop('current_property', None)
        super().__init__(*args, **kwargs)

        # Filter rooms by current property
        if current_property:
            self.fields['room'].queryset = Room.objects.filter(property=current_property)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
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
            FormActions(
                Submit('submit', _('Dodaj postęp'), css_class='btn btn-success btn-lg'),
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
        current_property = kwargs.pop('current_property', None)
        super().__init__(*args, **kwargs)

        # Filter rooms by current property
        if current_property:
            self.fields['rooms_worked_on'].queryset = Room.objects.filter(property=current_property)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
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
            Row(
                Column('rooms_worked_on', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz sesję'), css_class='btn btn-warning btn-lg'),
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
        current_property = kwargs.pop('current_property', None)
        super().__init__(*args, **kwargs)

        # Filter rooms by current property
        if current_property:
            self.fields['room'].queryset = Room.objects.filter(property=current_property)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
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
            )
        )


class RoomForm(forms.ModelForm):
    """Form for creating/editing rooms with all details"""

    # Multi-select for wall finishes (choices loaded dynamically)
    wall_finishes_multi = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label=_('Wykończenie ścian')
    )

    class Meta:
        model = Room
        fields = [
            'name', 'short_name', 'width', 'length', 'height', 'square_meters',
            'floor_type', 'current_status', 'future_plans', 'progress_notes',
            'progress_percentage', 'description'
        ]
        widgets = {
            'name': forms.Select(attrs={'id': 'id_name', 'class': 'form-control'}),
            'current_status': forms.Textarea(attrs={'rows': 3}),
            'future_plans': forms.Textarea(attrs={'rows': 3}),
            'progress_notes': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'progress_percentage': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load dynamic choices from DropdownChoice model
        try:
            room_choices = DropdownChoice.get_choices_for_type('room_type')
            if room_choices:
                self.fields['name'].choices = room_choices

            floor_choices = DropdownChoice.get_choices_for_type('floor_type')
            if floor_choices:
                self.fields['floor_type'].choices = [('', '---------')] + floor_choices

            wall_finish_choices = DropdownChoice.get_choices_for_type('wall_finish')
            if wall_finish_choices:
                self.fields['wall_finishes_multi'].choices = wall_finish_choices
            else:
                # Fallback to hardcoded choices if no dynamic choices exist
                self.fields['wall_finishes_multi'].choices = Room.WALL_FINISH_CHOICES
        except:
            # Fallback to hardcoded choices if DropdownChoice table doesn't exist
            self.fields['wall_finishes_multi'].choices = Room.WALL_FINISH_CHOICES

        # Pre-populate wall finishes from stored value
        if self.instance and self.instance.wall_finishes:
            self.fields['wall_finishes_multi'].initial = self.instance.wall_finishes.split(',')

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('short_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('width', css_class='form-group col-md-3 mb-3'),
                Column('length', css_class='form-group col-md-3 mb-3'),
                Column('height', css_class='form-group col-md-3 mb-3'),
                Column('square_meters', css_class='form-group col-md-3 mb-3'),
            ),
            Row(
                Column('floor_type', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('wall_finishes_multi', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('progress_percentage', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('current_status', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('progress_notes', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('future_plans', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz pomieszczenie'), css_class='btn btn-primary btn-lg'),
            )
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Convert multi-select wall finishes to comma-separated string
        wall_finishes = self.cleaned_data.get('wall_finishes_multi', [])
        instance.wall_finishes = ','.join(wall_finishes)
        if commit:
            instance.save()
        return instance


class PropertyForm(forms.ModelForm):
    """Form for creating/editing properties"""

    class Meta:
        model = Property
        fields = ['name', 'street_address', 'postal_code', 'city', 'country', 'description',
                  'renovation_start_date', 'renovation_end_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'renovation_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'renovation_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('street_address', css_class='form-group col-md-8 mb-3'),
                Column('postal_code', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-3'),
                Column('country', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('renovation_start_date', css_class='form-group col-md-6 mb-3'),
                Column('renovation_end_date', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz nieruchomość'), css_class='btn btn-primary btn-lg'),
            )
        )


class DropdownChoiceForm(forms.ModelForm):
    """Form for managing dropdown choices"""

    class Meta:
        model = DropdownChoice
        fields = ['choice_type', 'value', 'label_pl', 'label_en', 'display_order', 'is_active']
        widgets = {
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('np. salon, plytki')}),
            'label_pl': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nazwa po polsku')}),
            'label_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nazwa po angielsku')}),
        }
        help_texts = {
            'display_order': _('Niższe liczby pojawiają się jako pierwsze (np. 1 pojawi się przed 5). Użyj wielokrotności 10 (10, 20, 30), aby łatwiej można było wstawiać nowe opcje później.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('choice_type', css_class='form-group col-md-6 mb-3'),
                Column('display_order', css_class='form-group col-md-3 mb-3'),
                Column('is_active', css_class='form-group col-md-3 mb-3'),
            ),
            Row(
                Column('value', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('label_pl', css_class='form-group col-md-6 mb-3'),
                Column('label_en', css_class='form-group col-md-6 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz opcję'), css_class='btn btn-primary btn-lg'),
            )
        )


class EquipmentForm(forms.ModelForm):
    """Form for adding/editing equipment"""

    class Meta:
        model = Equipment
        fields = [
            'name', 'purpose', 'condition', 'is_old',
            'purchase_date', 'purchase_price', 'vendor', 'receipt_photo',
            'is_sold', 'sold_date', 'sold_price', 'notes'
        ]
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sold_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-8 mb-3'),
                Column('condition', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('purpose', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('is_old', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('purchase_date', css_class='form-group col-md-4 mb-3'),
                Column('purchase_price', css_class='form-group col-md-4 mb-3'),
                Column('vendor', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('receipt_photo', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('is_sold', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('sold_date', css_class='form-group col-md-6 mb-3'),
                Column('sold_price', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz sprzęt'), css_class='btn btn-primary btn-lg'),
            )
        )


class EquipmentPhotoForm(forms.ModelForm):
    """Form for uploading equipment photos"""

    class Meta:
        model = EquipmentPhoto
        fields = ['photo', 'caption']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('photo', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('caption', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Dodaj zdjęcie'), css_class='btn btn-success btn-lg'),
            )
        )


class EquipmentAssignmentForm(forms.ModelForm):
    """Form for assigning equipment to property"""

    class Meta:
        model = EquipmentAssignment
        fields = ['assigned_property', 'start_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter properties by user
        if user:
            self.fields['assigned_property'].queryset = Property.objects.filter(owner=user, is_active=True)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('assigned_property', css_class='form-group col-md-6 mb-3'),
                Column('start_date', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('notes', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Przypisz do nieruchomości'), css_class='btn btn-primary btn-lg'),
            )
        )


class RenovationTaskForm(forms.ModelForm):
    """Form for adding/editing renovation tasks"""

    class Meta:
        model = RenovationTask
        fields = ['title', 'description', 'room', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        current_property = kwargs.pop('current_property', None)
        super().__init__(*args, **kwargs)

        # Filter rooms by current property
        if current_property:
            self.fields['room'].queryset = Room.objects.filter(property=current_property)
            self.fields['room'].required = False

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('room', css_class='form-group col-md-6 mb-3'),
                Column('priority', css_class='form-group col-md-3 mb-3'),
                Column('status', css_class='form-group col-md-3 mb-3'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz zadanie'), css_class='btn btn-success btn-lg'),
            )
        )


class ShoppingItemForm(forms.ModelForm):
    """Form for adding/editing shopping items"""

    class Meta:
        model = ShoppingItem
        fields = ['title', 'description', 'room', 'vendor', 'quantity', 'unit', 'estimated_price', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        current_property = kwargs.pop('current_property', None)
        super().__init__(*args, **kwargs)

        # Filter rooms by current property
        if current_property:
            self.fields['room'].queryset = Room.objects.filter(property=current_property)
            self.fields['room'].required = False

        # Make vendor a dropdown with choices from DropdownChoice
        vendor_choices = DropdownChoice.get_choices_for_type('vendor')
        if vendor_choices:
            self.fields['vendor'] = forms.ChoiceField(
                choices=[('', '---------')] + vendor_choices,
                required=False,
                label=_('Sklep')
            )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('room', css_class='form-group col-md-6 mb-3'),
                Column('vendor', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('quantity', css_class='form-group col-md-4 mb-3'),
                Column('unit', css_class='form-group col-md-4 mb-3'),
                Column('estimated_price', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('priority', css_class='form-group col-md-6 mb-3'),
                Column('status', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
            ),
            FormActions(
                Submit('submit', _('Zapisz przedmiot'), css_class='btn btn-primary btn-lg'),
            )
        )
