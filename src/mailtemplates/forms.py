from django import forms
from .models import Category, MailTemplate
from django_summernote.widgets import SummernoteWidget
from django.utils.text import slugify

class CategoryForm(forms.ModelForm):
     class Meta:
         model = Category
         fields = '__all__'

class TemplateForm(forms.ModelForm):
    new_category_title = forms.CharField(required=False, label="Nueva categoría")
    slug = forms.CharField(required=False)

    class Meta:
        model = MailTemplate
        fields = ["title", "year", "category", "new_category_title", "subject", "content", "slug"]
        widgets = {
        'content': SummernoteWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        category = cleaned_data.get("category")
        new_category_title = cleaned_data.get("new_category_title")
        year = cleaned_data.get("year")

        # If a new category title is provided, create a new category and use it for the agenda
        if title:
            if Category.objects.filter(title=title).exists():
                self.add_error(
                    "title", "Ya existe una agenda con este nombre."
                )
            elif Category.objects.filter(slug=slugify(title)).exists():
                self.add_error(
                    "title",
                    "Ya existe una agenda con el slug generado a partir de este nombre.",
                )
            else:
                slug = slugify(f'{category}-{year}-{title}')
                cleaned_data["slug"] = slug

        # If a new category title is provided, create a new category and use it for the agenda
        if new_category_title and not category:
            if Category.objects.filter(title=new_category_title).exists():
                self.add_error(
                    "new_category_title", "Ya existe una categoria con este nombre."
                )
            elif Category.objects.filter(slug=slugify(new_category_title)).exists():
                self.add_error(
                    "new_category_title",
                    "Ya existe una categoria con el slug generado a partir de este nombre.",
                )
            else:
                slug = slugify(new_category_title)
                category = Category.objects.create(title=new_category_title, slug=slug)
                cleaned_data["category"] = category

        # If no category is selected and no new category title is provided, raise a validation error
        elif not category:
            self.add_error(
                "category", "Please select an existing category or create a new one."
            )

        return cleaned_data