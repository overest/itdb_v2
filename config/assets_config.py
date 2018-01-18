'''资产查询页面列表表单配置文件'''
query_table_config = [
    {
        'field':'asset_attr_id__asset_attr',
        'stitle':'资产属性',
        'display':1,
    },
    {
        'field': 'asset_id',
        'stitle': '资产编号',
        'display': 1,
    },
    {
        'field': 'sn',
        'stitle': '资产SN',
        'display': 1,
    },
    {
        'field': 'asset_model_id__asset_model',
        'stitle': '资产类别',
        'display': 1,
    },
    {
        'field': 'device_model_id__model_name',
        'stitle': '资产型号',
        'display': 1,
    },
    {
        'field': 'asset_status_id__asset_status',
        'stitle': '资产状态',
        'display': 1,
    },
    {
        'field': 'user_name_id__username',
        'stitle': '使用人',
        'display': 1,
    },
    {
        'field':'office_place_id__office_place',
        'stitle':'办公地点',
        'display':1,
    },
    {
        'field':'update_time',
        'stitle':'更新时间',
        'display':1,
    },
    {
        'field':'remark',
        'stitle':'备注',
         'display':1,
    }
]

'''资产详情表字段配置文件'''
asset_info_config = [
    {
        'field':'id',
        'stitle':'ID',
        'display':0,
    },
    {
        'field': 'asset_id',
        'stitle': '资产编号',
        'display': 1,
    },
    {
        'field': 'company_info',
        'stitle': '公司信息',
        'display': 1,
    },
    {
        'field': 'product_conf',
        'stitle': '配置信息',
        'display': 1,
    },
    {
        'field':'sn',
        'stitle':'资产序列号（S/N）',
        'display':1,
    },
    {
        'field': 'mac_addr',
        'stitle': 'MAC地址',
        'display': 1,
    },
    {
        'field': 'level',
        'stitle': '分类级别',
        'display': 0,
    },
    {
        'field': 'asset_attr',
        'stitle': '资产属性',
        'display': 1,
    },
    {
        'field': 'asset_model',
        'stitle': '资产类型',
        'display': 1,
    },
    {
        'field': 'asset_provider',
        'stitle': '品牌',
        'display': 1,
    },
    {
        'field': 'device_model',
        'stitle': '设备型号',
        'display': 1,
    },
    {
        'field': 'asset_name',
        'stitle': '资产名称',
        'display': 1,
    },
    {
        'field': 'office_place',
        'stitle': '办公地点',
        'display': 1,
    },
    {
        'field': 'store_place',
        'stitle': '库存地点',
        'display': 1,
    },
    {
        'field': 'use_type',
        'stitle': '使用类型',
        'display': 1,
    },
    {
        'field': 'asset_status',
        'stitle': '资产状态',
        'display': 1,
    },
    {
        'field': 'in_out_reason',
        'stitle': '出入库原因',
        'display': 1,
    },
    {
        'field': 'supplier',
        'stitle': '供应商',
        'display': 1,
    },
    {
        'field': 'last_check_time',
        'stitle': '上一次盘点时间',
        'display': 1,
    },
    {
        'field': 'user_name',
        'stitle': '使用人',
        'display': 1,
    },
    {
        'field': 'owner',
        'stitle': '责任人',
        'display': 1,
    },
    {
        'field': 'operator',
        'stitle': '最近操作人',
        'display': 1,
    },
    {
        'field': 'buy_time',
        'stitle': '购买时间',
        'display': 1,
    },
    {
        'field': 'create_time',
        'stitle': '创建时间',
        'display': 1,
    },
    {
        'field': 'update_time',
        'stitle': '更新时间',
        'display': 1,
    },
    {
        'field': 'up_time',
        'stitle': '启用时间',
        'display': 1,
    },
    {
        'field': 'remark',
        'stitle': '备注',
        'display': 1,
    }
    ]