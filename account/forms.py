from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="用户名",
        error_messages={'required':'请输入用户名'},
        widget = forms.TextInput(
            attrs={
                "placeholder":'用户名',
                'class': 'form-control',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="密码",
        error_messages={'required':'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'密码',
                'class': 'form-control',
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('用户名和密码为必填项')
        else:
            cleaned_data=super(LoginForm,self).clean()


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label='原密码',
        error_messages={'required':'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'原密码',
                'class': 'form-control',
            }
        ),
    )

    newpassword = forms.CharField(
        required=True,
        label='新密码',
        error_messages={'required': '请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '新密码',
                'class': 'form-control',
            }
        ),
    )

    newpassword1 = forms.CharField(
        required=True,
        label='确认密码',
        error_messages={'required': '请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '确认密码',
                'class': 'form-control',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('所有密码为必填项')
        elif self.cleaned_data['newpassword'] != self.cleaned_data['newpassword1']:
            raise forms.ValidationError("两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm,self).clean()
        return cleaned_data