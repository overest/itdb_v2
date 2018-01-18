from django.forms import Form
from django.forms import widgets
from  django.forms import fields


class AssetQuery(Form):
    search_key = fields.CharField(
        required=True,
        label=False,
        widget=widgets.TextInput(
            attrs={
                "placeholder": '请输入资产编号/资产序列号（sn）/MAC地址',
                'class': 'form-control search-query',
                # 'value':,
            }
        ),
    )

class AssetDetailInfo(Form):
    asset_id = fields.CharField(
        label="资产编号",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    asset_model = fields.CharField(
        label="资产类别",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly':'true',
            }
        ),
    )
    asset_provider = fields.CharField(
        label="资产品牌",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    device_model = fields.CharField(
        label="设备型号",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    mac_addr = fields.CharField(
        label="MAC地址",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    sn = fields.CharField(
        label="资产序列号（S/N）",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    asset_status = fields.CharField(
        label="资产状态",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    store_place = fields.CharField(
        label="库存地点",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    user_name = fields.CharField(
        label="使用人",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    owner = fields.CharField(
        label="责任人",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    office_place = fields.CharField(
        label="办公地点",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    in_out_reason = fields.CharField(
        label="出库原因",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    asset_attr = fields.CharField(
        label="资产属性",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    asset_name = fields.CharField(
        label="资产名称",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    product_conf = fields.CharField(
        label="配置信息",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    buy_time = fields.CharField(
        label="购买时间",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    supplier = fields.CharField(
        label="供应商",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    company_info = fields.CharField(
        label="公司信息",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    remark = fields.CharField(
        label="备注信息",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
    update_time = fields.CharField(
        label="更新时间",
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'true',
            }
        ),
    )
from assets import models
class Asset_out(Form):
    asset_id_field = fields.CharField(
        label="资产编号",
        required=True,
        widget=fields.TextInput(
            attrs={
                "class": "form-control",
                "readonly":True
            }
        )
    )
    use_type_field = fields.CharField(
        label="使用类型",
        initial=2,
        required=True,
        widget=widgets.Select
    )
    asset_status_field = fields.CharField(
        label="资产状态",
        initial=2,
        required=True,
        widget = widgets.Select
    )
    out_reason_field = fields.CharField(
        label="出库原因",
        initial=2,
        required=True,
        widget=widgets.Select
    )
    store_place_field = fields.CharField(
        label="库存地点",
        initial=2,
        required=True,
        widget=fields.Select
    )
    user_name_field = fields.CharField(
        label="使用人",
        required=True,
        widget=widgets.TextInput(
            attrs={
                "class": "form-control",
                'placeholder':"请输入使用人"
            }
        )
    )
    office_place_field = fields.CharField(
        label="办公地点",
        required=True,
        widget=fields.TextInput(
            attrs={
                "class": "form-control",
                "readonly":True
            }
        )
    )
    remark_info = fields.CharField(
        label="备注信息",
        required=False,
        widget=widgets.TextInput(
            attrs={
                "class": "form-control",
                'placeholder': "请输入备注信息"
            }
        )
    )
    def __init__(self,current_user,*args,**kwargs):
        super(Asset_out,self).__init__(*args,**kwargs)
        self.current_user = current_user
        self.fields['use_type_field'].widget.choices = models.UseType.objects.all().values_list('id', 'use_type')
        self.fields['use_type_field'].widget.attrs = {"class": "form-control"}
        self.fields['asset_status_field'].widget.choices = models.NonStock.objects.all().values_list('non_stock__id','non_stock__asset_status')
        self.fields['asset_status_field'].widget.attrs = {"class":"form-control"}
        self.fields['out_reason_field'].widget.choices = models.OutReasons.objects.all().values_list('out_reasons__id','out_reasons__in_out_reasons')
        self.fields['out_reason_field'].widget.attrs = {"class": "form-control"}
        self.fields['store_place_field'].widget.choices = models.UserProfile.objects.get(username=current_user).store_place.all().values_list('id', 'store_place')
        self.fields['store_place_field'].widget.attrs = {"class": "form-control"}
