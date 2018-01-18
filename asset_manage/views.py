from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from assets.models import AssetInfo,UserProfile,OperationLogs,AssetAttr,AssetModel,AssetName,AssetProvider,AssetStatus,DeviceModel,InOutReasons,Level,OfficePlace,ProductConf,StorePlace,Supplier,UseType
# from assets import models
from datetime import datetime,date

from django.http import StreamingHttpResponse

from django.db.models import Q

import time
import xlwt
import json
from io import BytesIO
# Create your views here.

from config import assets_config
class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None


class CJsonEncoder(json.JSONEncoder):
    '''Queryset 对象中datetime对象无法json序列化， 重写json序列化方法'''
    def default(self, o):
        if isinstance(o,datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o,date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self,o)


class Asset_manage_json(View):

    def get(self,request,asset_id,*args,**kwargs):
        response = BaseResponse()
        # data_obj = list(AssetInfo.objects.filter(asset_id=asset_id).values())
        # data_obj_2json = json.dumps(data_obj,cls=CJsonEncoder)
        # print(data_obj_2json)
        # return HttpResponse(data_obj_2json,content_type="application/json")
        try:
            asset_detail_conf = assets_config.asset_info_config
            field_list = []
            stitles = {}
            for item in asset_detail_conf:
                if item['display']:
                    field_list.append(item['field'])
                    stitles[item['field']] =item['stitle']
            # data_back = list(AssetInfo.objects.filter(asset_id=asset_id).values_list(*field_list))
            # #序列化
            # data_back_2json = json.dumps(data_back,cls=CJsonEncoder)
            # print(data_back)
            # return HttpResponse(data_back_2json)

            data_obj = AssetInfo.objects.get(asset_id=asset_id)
            data_dict = dict(
                asset_id=data_obj.asset_id,
                sn = data_obj.sn,
                mac_addr = data_obj.mac_addr,
                level = data_obj.level.level_name,
                asset_attr = data_obj.asset_attr.asset_attr,
                asset_model = data_obj.asset_model.asset_model,
                asset_provider = data_obj.asset_provider.provider,
                device_model = data_obj.device_model.model_name,
                product_conf = data_obj.product_conf.product_conf,
                asset_name = data_obj.asset_name.asset_name,
                office_place = data_obj.office_place.office_place,
                store_place = data_obj.store_place.store_place,
                use_type = data_obj.use_type.use_type,
                asset_status = data_obj.asset_status.asset_status,
                in_out_reason = data_obj.in_out_reason.in_out_reasons,
                supplier = data_obj.supplier.supplier,
                last_check_time = data_obj.last_check_time.check_time,
                user_name = data_obj.user_name.username,
                owner = data_obj.owner.username,
                operator = data_obj.operator.username,
                company_info = data_obj.company_info,
                buy_time = data_obj.buy_time,
                update_time = data_obj.update_time,
                create_time = data_obj.create_time,
                up_time = data_obj.up_time,
                remark = data_obj.remark
            )
            data_back = {}
            for key,val in data_dict.items():
                if key in field_list:
                    data_back[key] = val
            data_back_dict = {
                "stitles":stitles,
                "data_back":data_back
            }
            data_back_2json = json.dumps(data_back_dict,cls=CJsonEncoder)
            response.data = data_back_2json
        except Exception as e:
            response.status = False
            response.message = str(e)
        return HttpResponse(json.dumps(response.__dict__))

class Operation_Logs_json(View):
    '''获取该设备的操作日志'''
    def get(self, request, asset_id, *args, **kwargs):
        response = BaseResponse()
        try:
            operation_logs_obj = OperationLogs.objects.filter(asset_id=asset_id).order_by("-update_time")

            operation_logs_list = []
            for item in operation_logs_obj:
                operation_logs_dict = {}
                operation_logs_dict['type'] = item.get_type_display()
                operation_logs_dict['before_field'] = item.before_field
                operation_logs_dict['update_time'] = item.update_time
                operation_logs_dict['after_field'] = item.after_field
                operation_logs_dict['operator'] = item.operator.username
                operation_logs_list.append(operation_logs_dict)
            print(operation_logs_list)
            operation_logs_2json = json.dumps(operation_logs_list,cls=CJsonEncoder)
            print(operation_logs_2json)
            response.data = operation_logs_2json
        except Exception as e:
            response.status = False
            response.message = str(e)
        return HttpResponse(json.dumps(response.__dict__))


class Asset_info_json(View):
    def post(self,request,*args,**kwargs):
        response = BaseResponse()
        search_val = request.body.decode("utf-8")
        print(search_val)
        try:
            search_data_obj = AssetInfo.objects.get(
                Q(asset_id=search_val)|Q(sn=search_val)|Q(mac_addr=search_val),
            )
            search_data = dict(
                asset_id=search_data_obj.asset_id,
                sn=search_data_obj.sn,
                mac_addr=search_data_obj.mac_addr,
                asset_attr=search_data_obj.asset_attr.asset_attr,
                asset_model=search_data_obj.asset_model.asset_model,
                asset_provider=search_data_obj.asset_provider.provider,
                device_model=search_data_obj.device_model.model_name,
                product_conf=search_data_obj.product_conf.product_conf,
                asset_name=search_data_obj.asset_name.asset_name,
                office_place=search_data_obj.office_place.office_place,
                store_place=search_data_obj.store_place.store_place,
    #             use_type=search_data_obj.use_type.use_type,
                asset_status=search_data_obj.asset_status.asset_status,
                in_out_reason=search_data_obj.in_out_reason.in_out_reasons,
                supplier=search_data_obj.supplier.supplier,
    #             last_check_time=search_data_obj.last_check_time.check_time,
                user_name=search_data_obj.user_name.username,
                owner=search_data_obj.owner.username,
    #             operator=search_data_obj.operator.username,
                company_info=search_data_obj.company_info,
                buy_time=search_data_obj.buy_time,
                update_time=search_data_obj.update_time,
    #             create_time=search_data_obj.create_time,
    #             up_time=search_data_obj.up_time,
                remark=search_data_obj.remark
            )
            search_data_dict = {
                "search_data":search_data
            }
            search_data_2json = json.dumps(search_data_dict,cls=CJsonEncoder)
            response.data = search_data_2json
        except Exception as e:
            response.status = False
            response.message = str(e)
        return HttpResponse(json.dumps(response.__dict__))


class User_info_json(View):
    def get(self,request,username,*args,**kwargs):
        response = BaseResponse()
        try:
            user_info_obj = UserProfile.objects.get(username=username)
            store_place = user_info_obj.store_place.values_list('store_place')
            user_info = dict(
                office_place = user_info_obj.office_place.office_place,
                store_place = store_place[0][0]
            )

            user_info_dict = {
                "user_info":user_info
            }
            user_info_2json = json.dumps(user_info_dict)
            response.data = user_info_2json

        except Exception as e:
            response.status = False
            response.message = str(e)
        return HttpResponse(json.dumps(response.__dict__))


class ExportAsset(View):


    def get(self,request,owner,*args,**kwargs):

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'AssetInfo-%s.xls' % (time.strftime('%Y-%m-%d',time.localtime(time.time())))
        wb = xlwt.Workbook(encoding="utf-8")
        sheet_assetinfo = wb.add_sheet("AssetInfo")
        style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """
                                    )


        style_body = xlwt.easyxf("""
            font:
                name Arial,
                bold off,
                height 0XA0;
            align:
                wrap on,
                vert center,
                horiz left;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """
                                 )
        style_body.num_format_str = 'yyyy-mm-dd hh:mm:ss'  #定义时间格式，xlwt读取数据库中的时间默认问float类型写入excel中

        heading = []
        if owner != "all":
            data_obj = AssetInfo.objects.filter(owner_id__username=owner)
        else:
            data_obj = AssetInfo.objects.all()
        print(data_obj[0].last_check_time.check_time.strftime('%Y-%m-%d %H:%M:%S'))
        for row in data_obj[0]._meta._get_fields():
            heading.append(row.verbose_name)
        for i in range(0,len(heading)):
            sheet_assetinfo.write(0,i,heading[i],style_heading)
        row = 1
        for content in data_obj:
            sheet_assetinfo.write(row, 0, content.asset_id, style_body)
            sheet_assetinfo.write(row, 1, content.sn, style_body)
            sheet_assetinfo.write(row, 2, content.mac_addr, style_body)
            sheet_assetinfo.write(row, 3, content.level.level_name, style_body)
            sheet_assetinfo.write(row, 4, content.asset_attr.asset_attr, style_body)
            sheet_assetinfo.write(row, 5, content.asset_model.asset_model, style_body)
            sheet_assetinfo.write(row, 6, content.asset_provider.provider, style_body)
            sheet_assetinfo.write(row, 7, content.device_model.model_name, style_body)
            sheet_assetinfo.write(row, 8, content.product_conf.product_conf, style_body)
            sheet_assetinfo.write(row, 9, content.asset_name.asset_name, style_body)
            sheet_assetinfo.write(row, 10, content.office_place.office_place, style_body)
            sheet_assetinfo.write(row, 11, content.store_place.store_place, style_body)
            sheet_assetinfo.write(row, 12, content.use_type.use_type, style_body)
            sheet_assetinfo.write(row, 13, content.asset_status.asset_status, style_body)
            sheet_assetinfo.write(row, 14, content.in_out_reason.in_out_reasons, style_body)
            sheet_assetinfo.write(row, 15, content.supplier.supplier, style_body)
            sheet_assetinfo.write(row, 16, content.last_check_time.check_time, style_body)

            sheet_assetinfo.write(row, 17, content.user_name.username, style_body)
            sheet_assetinfo.write(row, 18, content.owner.username, style_body)
            sheet_assetinfo.write(row, 19, content.operator.username, style_body)
            sheet_assetinfo.write(row, 20, content.company_info, style_body)
            sheet_assetinfo.write(row, 21, content.buy_time.strftime('%Y-%m-%d %H:%M:%S'), style_body)
            sheet_assetinfo.write(row, 22, content.create_time.strftime('%Y-%m-%d %H:%M:%S'), style_body)
            sheet_assetinfo.write(row, 23, content.update_time.strftime('%Y-%m-%d %H:%M:%S'), style_body)
            sheet_assetinfo.write(row, 24, content.up_time.strftime('%Y-%m-%d %H:%M:%S'), style_body)
            sheet_assetinfo.write(row, 25, content.remark, style_body)
            row += 1
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        response.write(output.getvalue())
        print(response)
        return response

from django.http import FileResponse
class Download_template(View):
    def get(self,request,file_name,*args,**kwargs):

        with open("/www/itdb_v2/static/excel/%s" %file_name,'rb') as file:
            response = FileResponse(file)
            response['Content-Type']='application/octet-stream'
            response['Content-Disposition']='attachment;filename="%s"' %file_name
        return response
