from django import forms


class UploadForm(forms.Form):
    file = forms.FileField(label="上传文件",
                           required=True,
                           help_text="在此处选择并上传文件")
