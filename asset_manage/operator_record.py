'''
资产信息操作（出库、入库、修改资产属性），h获取OperatorLog表中before_field列、after_field列
'''
import requests,json
def get_before_field(asset_id):
    '''获取OperatorLog表中before_field列'''
    get_before_asset_info = requests.get("http://127.0.0.1:8000/asset_manage/asset_manage/id/%s/" % asset_id)
    before_asset_info = {}
    before_asset_info_data = json.loads(json.loads(get_before_asset_info.content.decode("utf-8"))['data'])[
        'data_back']
    current_asset_info_stitle = json.loads(json.loads(get_before_asset_info.content.decode("utf-8"))['data'])[
        'stitles']
    for en_title, ch_title in current_asset_info_stitle.items():
        for k, v in before_asset_info_data.items():
            if k == en_title:
                before_asset_info[ch_title] = v
            else:
                continue
    return before_asset_info

def get_after_field(asset_id):
    '''获取OperatorLog表中after_field列'''
    get_current_asset_info = requests.get("http://127.0.0.1:8000/asset_manage/asset_manage/id/%s/" % asset_id)  # 获取入库后的资产详情，将其写入OperationLogs数据表
    current_asset_info = {}
    current_asset_info_data = json.loads(json.loads(get_current_asset_info.content.decode("utf-8"))['data'])[
        'data_back']
    current_asset_info_stitle = json.loads(json.loads(get_current_asset_info.content.decode("utf-8"))['data'])[
        'stitles']
    for en_title, ch_title in current_asset_info_stitle.items():
        for k, v in current_asset_info_data.items():
            if k == en_title:
                current_asset_info[ch_title] = v
            else:
                continue

    return current_asset_info
