from django import forms


class UploadForm(forms.Form):
    file = forms.FileField(label="上传文件",
                           required=True,
                           help_text="在此处选择并上传文件",
                           widget=forms.FileInput(attrs={'class': 'form-control'}))
    filename = forms.CharField(label="文件名",
                               required=True,
                               help_text="您可以手动指定一个文件名",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
