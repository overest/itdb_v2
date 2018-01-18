from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
import json
import time
from assets.models import AssetInfo,UserProfile,OfficePlace,OperationLogs,AssetStatus,UseType,InOutReasons,StorePlace
from .forms import AssetQuery,AssetDetailInfo,Asset_out

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from asset_manage import operator_record
import xlrd
# Create your views here.
class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None


# class CJsonEncoder(json.JSONEncoder):
#     '''Queryset 对象中datetime对象无法json序列化， 重写json序列化方法'''
#     def default(self, o):
#         if isinstance(o,datetime):
#             return o.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(o,date):
#             return o.strftime('%Y-%m-%d')
#         else:
#             return json.JSONEncoder.default(self,o)


class Stock_out(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):

        asset_id = request.GET.get('asset_id')

        search_form = AssetQuery()
        asset_detail_info_form = AssetDetailInfo()
        asset_out_form = Asset_out(request.user.username)
        return render(request, "assets/stock_out/stock_out.html",
                      {"search_form": search_form, "stitle": "资产出库", "asset_detail_info_form": asset_detail_info_form,
                       'asset_out_form': asset_out_form,'asset_id':asset_id})

    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        response = BaseResponse()
        user_perms = request.user.get_all_permissions()    #获取当前登录用户的所有权限
        #获取出库前的资产详细信息
        req_data = json.loads(request.body.decode('utf-8'))

        print(req_data)
        ##OperationLogs表中before_field
        before_field = operator_record.get_before_field(req_data['asset_id_field'])

        if "assets.change_assetinfo" in user_perms:
            try:
                update_filds_dict = {}
                update_filds_dict['operator_id'] = UserProfile.objects.filter(username=request.user.username).values()[0]["id"]
                update_filds_dict['owner_id'] = UserProfile.objects.filter(username=req_data['user_name_field']).values()[0]["id"]
                update_filds_dict['user_name_id'] = UserProfile.objects.filter(username=req_data['user_name_field']).values()[0]["id"]
                update_filds_dict['asset_status_id'] = req_data['asset_status_field']
                update_filds_dict['office_place_id'] = OfficePlace.objects.filter(office_place=req_data['office_place_field']).values()[0]["id"]
                update_filds_dict['remark'] = req_data['remark_info']
                update_filds_dict['use_type_id'] = req_data['use_type_field']
                update_filds_dict['in_out_reason_id'] = req_data['out_reason_field']
                update_filds_dict['store_place_id'] = req_data['store_place_field']
                update_filds_dict['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                #更新AssetInfo表
                AssetInfo.objects.filter(asset_id=req_data['asset_id_field']).update(**update_filds_dict)

                # OperationLogs表中after_field
                after_field = operator_record.get_after_field(req_data['asset_id_field'])

                operation_record = {"asset_id": req_data['asset_id_field'],"type": "1",'before_field':before_field,"after_field":after_field, 'operator': request.user}
                OperationLogs.objects.create(**operation_record)
                response.data = {'resp':"ok"}
            except Exception as e:
                response.status = False
                response.message = str(e)
            return HttpResponse(json.dumps(response.__dict__))
        else:
            response.status = False
            return HttpResponse("滚！")

class Batch_stock_out(View):
    '''批量出库'''
    def post(self,request,*args,**kwargs):

        upload_file = request.FILES
        print(upload_file)

        model_filed = ['asset_id','use_type','asset_status','in_out_reason','user_name','remark']
        wb = xlrd.open_workbook(filename=None, file_contents=upload_file['file[0]'].read())
        sheet = wb.sheet_by_name('AssetInfo')
        row = sheet.nrows
        #
        for i in range(1, row):
            row_vals = sheet.row_values(i)
            update_dict = dict(zip(model_filed,row_vals))
            print(update_dict)
            ##OperationLogs表中before_field
            before_field = operator_record.get_before_field(update_dict['asset_id'])

            # 更新AssetInfo 字段字典
            update_dict_2db = {}
            update_dict_2db['operator_id'] = UserProfile.objects.filter(username=request.user.username).values()[0]["id"]
            update_dict_2db['owner_id'] = UserProfile.objects.filter(username=request.user.username).values()[0]["id"]
            update_dict_2db['user_name_id'] = UserProfile.objects.filter(username=update_dict['user_name']).values()[0]["id"]
            update_dict_2db['asset_status_id'] = AssetStatus.objects.filter(asset_status=update_dict['asset_status']).values()[0]['id']
            update_dict_2db['office_place_id'] = OfficePlace.objects.filter(office_place_user__username=update_dict['user_name']).values()[0]["id"]
            update_dict_2db['remark'] = update_dict['remark']
            update_dict_2db['use_type_id'] = UseType.objects.filter(use_type=update_dict['use_type']).values()[0]['id']
            update_dict_2db['in_out_reason_id'] = InOutReasons.objects.filter(in_out_reasons=update_dict['in_out_reason']).values()[0]['id']
            update_dict_2db['store_place_id'] = StorePlace.objects.filter(store_place_user__username=request.user.username).values()[0]['id']
            update_dict_2db['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            AssetInfo.objects.filter(asset_id=update_dict['asset_id']).update(**update_dict_2db)

            # OperationLogs表中after_field
            after_field = operator_record.get_after_field(update_dict['asset_id'])

            operation_record = {"asset_id": update_dict['asset_id'], "type": "1", 'before_field': before_field,"after_field": after_field, 'operator': request.user}
            OperationLogs.objects.create(**operation_record)

        return HttpResponse(request.FILES)
