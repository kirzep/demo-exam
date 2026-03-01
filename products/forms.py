from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' # Берем все поля из модели
        
    # Стилизуем поля прямо из Питона, чтобы не писать CSS в HTML
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['style'] = 'padding: 8px; width: 100%; margin-bottom: 10px; box-sizing: border-box;'

    # Кастомная валидация: цена не может быть отрицательной
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля!")
        return price

    # Скидка не может быть больше 100%
    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount < 0 or discount > 100:
            raise forms.ValidationError("Скидка должна быть от 0 до 100%.")
        return discount