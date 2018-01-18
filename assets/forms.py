from django.forms import fields,Form

class AssetQuery(Form):
    search_key = fields.CharField(
        required=True,
        label=False,
        error_messages={'required': '请输入需要查询的用户'},
        widget=fields.TextInput(
            attrs={
                "placeholder": '请输入用户名',
                'class': 'form-control search-query',
            }
        ),
    )