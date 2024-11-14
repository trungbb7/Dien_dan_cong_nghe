from django import forms


from django import forms

class QuestionForm(forms.Form):
    question_title = forms.CharField(label='Tiêu đề câu hỏi', max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control_question_title',
        'placeholder': 'Nhập tiêu đề câu hỏi của bạn'
    }))
    question_description = forms.CharField(label='Mô tả câu hỏi', widget=forms.Textarea(attrs={
        'class': 'form-control_question_description',
        'placeholder': 'Mô tả chi tiết câu hỏi của bạn'
    }))
    related_tags = forms.CharField(label='Thẻ liên quan', max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control_related_tags',
        'placeholder': 'Thêm các thẻ liên quan, cách nhau bằng dấu phẩy'
    }))
