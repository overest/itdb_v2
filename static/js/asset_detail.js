/**
 * Created by Gary on 2017/11/22.
 */

//asset_query
(function (jq) {
    function show_asset_table(url) {
        var asset_table = $("#asset_list_table");
        if($.fn.dataTable.fnIsDataTable(asset_table)){
            $(asset_table).dataTable().fnDestroy();
        }
        var aoColumns = [{
                "mData" : "asset_attr_id__asset_attr",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "10%"
            },{
                "mData" : "asset_id",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "15%"
            },{
                "mData" : "sn",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "20%"
            },{
                "mData" : "asset_model_id__asset_model",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "5%"
            },{
                "mData" : "device_model_id__model_name",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "5%"
            },{
                "mData" : "asset_status_id__asset_status",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "5%"
            },{
                "mData" : "user_name_id__username",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "5%"
            },{
                "mData" : "office_place_id__office_place",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "5%"
            },{
                "mData" : "update_time",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "20%",
            },{
                "mData" : "remark",
                "orderable": false , // 禁用排序
                "sDefaultContent" : "",
                "sWidth" : "10%"
            }];
        var oTable = $(asset_table).dataTable(
            {
                "aLengthMenu":[10,20,40,60],
                "searching":false,//禁用搜索
                "lengthChange":true ,
                "paging": true,//开启表格分页
                "bProcessing" : false,
                "ServerSide" : true,
                "bAutoWidth" : true,
                "bSort" : false,
                "deferRender":true,//延迟渲染
                "bStateSave" : false, //在第三页刷新页面，会自动到第一页
                "iDisplayLength" : 10,
                "iDisplayStart" : 0,
                "dom": '<l<\'#topPlugin\'>f>rt<ip><"clear">',
                "ordering" : false,   //全局禁用排序
                "aoColumns":aoColumns,
                "sAjaxSource": url,
                "fnServerData": function (sSource, aDataSet, fnCallback) {
                    $.ajax({
                        "dataType": 'json',
                        "type": "POST",
                        "url": sSource,
                        "data": aDataSet,

                        "success": function (resp) {
                            var queryData = $.parseJSON(JSON.parse(resp.data).query_data);
                            var conf = JSON.parse(resp.data).config;
                            asset_list_table_head(conf);  //生成表头
                            var data = {"aaData":queryData};
                            fnCallback(data)
                        }
                    });
                },
                "fnDrawCallback":function () {
                    if(!oTable){
                        return;
                    }
                    oTable.$("tr").unbind('click');
                    oTable.$("tr").click({oTable:oTable},function (e) {
                        if ($(this).hasClass('row_selected')) {
                            $(this).removeClass('row_selected');
                        } else {
                            e.data.oTable.$('tr.row_selected').removeClass('row_selected');
                            $(this).addClass('row_selected');
                            var asset_id = e.data.oTable.fnGetData(this)["asset_id"];
                            var asset_status = e.data.oTable.fnGetData(this)['asset_status_id__asset_status'];
                            show_asset_details_table(asset_id,asset_status);
                            show_asset_log_table(asset_id)
                        }
                    })
                },


                "oLanguage" : { // 国际化配置
                "sProcessing" : "正在获取数据，请稍后...",
                "sLengthMenu" : "显示 _MENU_ 条",
                "sZeroRecords" : "没有找到数据",
                "sInfo" : "从 _START_ 到  _END_ 条记录 总记录数为 _TOTAL_ 条",
                "sInfoEmpty" : "记录数为0",
                "sInfoFiltered" : "(全部记录数 _MAX_ 条)",
                "sInfoPostFix" : "",
                "sSearch" : "搜索",
                "sUrl" : "",
                "oPaginate" : {
                    "sFirst" : "第一页",
                    "sPrevious" : "上一页",
                    "sNext" : "下一页",
                    "sLast" : "最后一页"
                }
                }
            }
        )
    }
    //显示右侧资产详情表格
    function show_asset_details_table(asset_id,asset_status) {
        var asset_detaile_table = $("#asset_detail_table");
        if($.fn.dataTable.fnIsDataTable(asset_detaile_table)){
            $(asset_detaile_table).dataTable().fnDestroy();
        };
        $("#asset_detail_table").dataTable({
            "bRetrieve": true,
            "bFilter": false,
            "bPaginate": false,
            "bSort": false,
            "sDom": 't',
            "bServerSide": false,
            "bAutoWidth": false,
            "sAjaxSource": "/asset_manage/asset_manage/id/" + asset_id + '/',
            "aoColumns": [
                {
                    "sTitle": "属性名", "sWidth": 150, "sClass": "text-center"
                },
                {
                    "sTitle": "属性值"
                }
            ],
            "fnServerData":function (sSource,aDataSet,fnCallback) {
                $.ajax({
                    "dataType":"json",
                    "type":"GET",
                    "url":sSource,
                    "data": aDataSet,
                    success:function (resp) {
                        if (asset_status == "在用"){
                            $("#si_dev_btn").removeClass("hide").attr("href","/stock_in/stock_in?asset_id="+asset_id);
                            $("#st_dev_btn").addClass("hide");
                        }
                        else {
                            $("#st_dev_btn").removeClass("hide").attr("href","/stock_out/stock_out?asset_id="+asset_id);
                            $("#si_dev_btn").addClass("hide");
                        }

                        var stitles = JSON.parse(resp.data).stitles;
                        var data_back = JSON.parse(resp.data).data_back;
                        var aaData = [];
                        $.each(stitles,function (k1,stitle) {
                            $.each(data_back,function (k2,val) {
                                if(k1==k2){
                                    aaData.push([stitle,val]);
                                }
                            })
                        });
                        var data = {'aaData':aaData};

                        fnCallback(data)

                    }
                })
            }

        })
    }
    //显示右侧资产操作信息
    function show_asset_log_table(asset_id) {
        var asset_log_table = $("#asset_log_table");
        if($.fn.dataTable.fnIsDataTable(asset_log_table)){
            $(asset_log_table).dataTable().fnDestroy()
        }
        $("#asset_log_table").dataTable({
            "aLengthMenu":[10,20,40,60],
            "searching":true,//禁用搜索
            "lengthChange":true ,
            "paging": false,//开启表格分页
            "bProcessing" : false,
            "ServerSide" : true,
            "bAutoWidth" : true,
            "bSort" : false,
            "deferRender":true,//延迟渲染
            "bStateSave" : false, //在第三页刷新页面，会自动到第一页
            "iDisplayLength" : 10,
            "iDisplayStart" : 0,
            "dom": '<l<\'#topPlugin\'>f>rt<ip><"clear">',
            "sAjaxSource":"/asset_manage/operation_logs/id/" + asset_id + "/",
            "aoColumns":[
                {
                    "sTitle":"操作类型","sWidth": 20, "sClass": "text-center",'mData':"type",
                },
                {
                    "sTitle":"操作人","sWidth": 20, "sClass": "text-center",'mData':"operator"
                },
                {
                    "sTitle":"操作时间","sWidth": 50, "sClass": "text-center",'mData':"update_time"
                },
                {
                    "sTitle":"操作内容","sClass": "text-center",'mData':"text"
                }
                ],
            "fnServerData":function (sSource,aDataSet,fnCallback) {
                $.ajax({
                    "dataType":"json",
                    "type":"GET",
                    "url":sSource,
                    "data":aDataSet,
                    success:function (resp) {if (resp.status){
                        var respData = JSON.parse(resp.data);
                        var aaData = [];
                        for(var i=0;i<respData.length;i++){
                            var aDict={};
                            var content1 = "";
                            var content2 = "";
                            var before_field_obj=eval("(" + respData[i].before_field + ")");
                            var after_field_obj =eval("(" + respData[i].after_field + ")");
                            var type = respData[i].type;
                            var operator = respData[i].operator;
                            var update_time = respData[i].update_time;

                            $.each(before_field_obj,function (k1,val1) {
                                $.each(after_field_obj,function (k2,val2) {
                                    if(k2 == k1){
                                        if(val2 == val1){
                                            content1 += "<dt>"+ k1 + ":" + val1 + "</dt>";
                                            content2 += "<dt>"+ k2 + ":" + val2 + "</dt>"
                                        }else {
                                            content1 += "<dt style='color:red'>"+ k1 + ":" + val1 + "</dt>";
                                            content2 += "<dt style='color:red'>"+ k2 + ":" + val2 + "</dt>"
                                        }
                                    }
                                })
                            });
                            var text = "<table><tbody><tr><th style='font-size: 15px;color: #28a4c9;'>"+ "修改前：" + "</th><th style='font-size: 15px;color: #28a4c9;'>" + "修改后：" + "</th></tr>"  +"<tr><th>" + content1 + "</th>" +"<th>" + content2 + "</th>" + "</tbody></table>";
                            aDict["type"] = type;
                            aDict["operator"] = operator;
                            aDict["update_time"] = update_time;
                            aDict["text"] = text;
                            aaData.push(aDict);
                        }
                        var data = {'aaData':aaData};
                        fnCallback(data)
                    }
                    }
                })
            },
            "oLanguage" : { // 国际化配置
                "sProcessing" : "正在获取数据，请稍后...",
                "sLengthMenu" : "显示 _MENU_ 条",
                "sZeroRecords" : "没有找到数据",
                "sInfo" : "从 _START_ 到  _END_ 条记录 总记录数为 _TOTAL_ 条",
                "sInfoEmpty" : "记录数为0",
                "sInfoFiltered" : "(全部记录数 _MAX_ 条)",
                "sInfoPostFix" : "",
                "sSearch" : "搜索",
                "sUrl" : "",
                "oPaginate" : {
                    "sFirst" : "第一页",
                    "sPrevious" : "上一页",
                    "sNext" : "下一页",
                    "sLast" : "最后一页"
                }
                }
        })
    }


    function asset_list_table_head(config) {
        var asset_table_head_th = $("#asset_table_head tr th");
        var headText = {};
        $.each(config,function (k1,v1) {
            headText[k1] = config[k1].stitle;
        });
        $.each(asset_table_head_th,function (k2,v2) {
            asset_table_head_th[k2].innerHTML = headText[k2]
        })
    }

    function init() {
        $("#search_button").click(function (event) {
            var query_username = $("#id_search_key").val();
            if ($("#id_search_key").val().length == "0") {
                $("#search_button").attr({"data-toggle": "modal", "data-target": "#myModal"});
            }else {
                var url="/assets/asset_query_json/" + query_username +'/';
                show_asset_table(url)
            }
        });

        //点击弹出框关闭按钮或'x'按钮时，取消查询按钮的data-toggle，data-target属性
        $("#off_modal,#x_x").bind('click',function () {
            $("#search_button").removeAttr("data-toggle");
            $("#search_button").removeAttr("data-target");
        });

    }

    jq.extend({
        'asset_detail_func':function () {
            init()
        }
    })
})(jQuery);
