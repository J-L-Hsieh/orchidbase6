$( document  ).ready(function() {
   $( document  ).ready(function() {
        $.ajaxSetup({
            data: {
                    csrfmiddlewaretoken: '{{ csrf_token  }}'                           
            },           
        });
        var href = window.location.href;
        var Type = href.split("=")[1];
        $("#Database").html("<option>"+ Type +"_pep</option>");
        //全域變數，用來存第一次的資料
        var table_data;
        var obj="";
        $("#btnblast").click(function(){
            $.blockUI({ css: {
                border: 'none',
                padding: '15px',
                backgroundColor: '#000',
                '-webkit-border-radius': '10px',
                '-moz-border-radius': '10px',
                opacity: .5,
                color: '#fff',
                message:"Loding..."
            } });

            $("#resultlabel").empty();
            var blast_type = $("#ProgramName").val();
            var database = $("#Database").val();
            var evalue = $("#ExpectThreshold").val();
            var num_alignments = $("#OfAlignment").val();
            var outfmt = $("#AlignmentView").val();
            var gapopen = $("#GapCosts").val();
            var gapextend =$("#GapExtcosts").val();

            var Parameters = {"blast_type":blast_type,"database":database,"evalue":evalue,"num_alignments":num_alignments,"outfmt":outfmt,"gapopen":gapopen,"gapextend":gapextend};
            //console.log(Parameters);
            var input_data = $("#txtinputSequence").val();

            //var type = "Phalaenopsis";
            $.ajax({
                url:'https://cosbi.ee.ncku.edu.tw/orchidbase6/expression_profiling/ajax_parse2/',
                data:{"Type":Type,'data':input_data,'Parameters':JSON.stringify(Parameters)},
                type:'POST',
                dataType:'json',
                success:function(data){                          
                    //console.log(data[0]);
                    $("#ShowExpressionProfile").show();

                    $("#resultlabel").html("<taple id='mytable' class='table table-bordered'></table>");//需放到ajax success 裡面不然格式會跑掉
                    create_blast_table(data[1],data[2],data[3],data[4],data[5],data[6],data[7]);

                    $('.view_detail').on("click",function(e){
                        //console.log("ok");
                        e.preventDefault();
                        $(this).parent().siblings().find('div').slideUp();
                        $(this).parent().find('div').slideToggle();
                    });

                    $('#CheckAll').click(function(){
                    //console.log("ok");
                    if($('#CheckAll').prop("checked"))//如果全選按鈕有被選擇的話（被選擇是true）
                      {
                        //console.log("checkbox is checked");
                       $("input[name='checkbox']").prop("checked",true);//把所有的核取方框的property都變成勾選
                      }
                    else
                      {
                       $("input[name='checkbox']").prop("checked",false);//把所有的核取方框的property都取消勾選
                      }
                    });
                    $.unblockUI(); //Loading...跑完後關掉
                },
                error:function(){
                    alert('Something error');
                    $.unblockUI(); //Loading...跑完後關掉
                },
                });
                  
        })

        $("#ProgramName").change(function(){
            var blast_type = $("#ProgramName").val(); 
            if(blast_type=="blastx"){
                $("#Button1").attr("value","Example:Peq023316").attr("onclick","AddTextboxes_blastx()");
            }
            else{
                $("#Button1").attr("value","Example:Peq006591").attr("onclick","AddTextboxes_blastp()");
            }
        })  


        $("#ShowExpressionProfile").click(function(){
            var arr=[];
            $("[name=checkbox]:checkbox:checked").each(function(){
            arr.push($(this).val());
            });
            var arr_string = JSON.stringify(arr);
            //console.log(arr_string);
            //console.log(typeof(arr_string));//string
            var type="";
            if (arr == null || arr.length == null || arr.length == 0) {
                alert("please check the Gene ID checkbox first");
            }
            else{
            $.blockUI({ css: {
                        border: 'none',
                        padding: '15px',
                        backgroundColor: '#000',
                        '-webkit-border-radius': '10px',
                        '-moz-border-radius': '10px',
                        opacity: .5,
                        color: '#fff',
                        message:"Loding..."
                    } });
                    //setTimeout($.unblockUI, 2000);//自行設定等待時間
                    /*
                    setTimeout(function (){
                      $("#${id}_table").setGridWidth($("#${id}_table_container").width(),true) // something that take some time.
                      $.unblockUI();      
                     }, 0);*/

            var select_data_type = $("#select_data_type").val(); 

            $.ajax({
                    url:'expression_profiling/ajax_parse3/',
                    data:{'data':arr_string,'select_data_type':select_data_type},
                    type:'POST',
                    dataType:'json',
                    success:function(data){  
                        table_data = data; 
                        
                        $("#expression_button").show();

                        //plot_table
                        $('#mydiv').empty();
                        $('#mydiv').html("<table id='myDataTable'  class='table table-hover dt-responsive order-columnmemberList tblFormat cell-border table-striped' ></table>");
                        create_table(data[2],data[3],data[4]);
                        //關閉ordering功能  
                        $('#myDataTable').DataTable({
                            "destroy": true,
                            "ordering":false,
                            "scrollX": true,
                            })

                        $('#checkall').click(function(){
                        //console.log("ok");
                        if($('#checkall').prop("checked"))//如果全選按鈕有被選擇的話（被選擇是true）
                          {
                            //console.log("ok");
                           //$("input[name='ID']").prop("checked",true);//把所有的核取方框的property都變成勾選，若有第二頁，此方法會出問題
                           $('#myDataTable').DataTable()
                                .column(0)
                                .nodes()
                                .to$()
                                .find('input[name=ID]')
                                .prop('checked', this.checked);//true
                          }
                        else
                          {
                           //$("input[name='ID']").prop("checked",false);//把所有的核取方框的property都取消勾選，若有第二頁，此方法會出問題
                           $('#myDataTable').DataTable()
                                .column(0)
                                .nodes()
                                .to$()
                                .find('input[name=ID]')
                                .prop('checked', false);
                          }
                        });
                        //plotheatmap
                        plotheatmap(data[2],data[3],data[4]); 

                        //plotcluster
                        if (data[5]=="no picture"){
                            document.getElementById("img").src="";
                            $("#img_table").hide();
                            $("#cluster_text").html("<b>Because the Gene expression data have some null value,the Cluster chart can't be displayed!</b>");
                        }
                        else{
                            document.getElementById("img").src="../../../t50504_static/img/heatmap/" + data[5] + ".png" //絕對路徑寫法，因為寫相對路徑會出錯
                            //document.getElementById("img").src="{% static 'img/heatmap/OktRM.png' %}"
                        }

                        //plotpca
                        if (data[6]=="no pca"){
                            $("#pca").empty();
                            $("#pca").html("<b>Because the Gene expression data have some null value or the Gene expression data only have one column,the PCA chart can't be displayed!</b>");
                        }
                        else{
                            plotpca(data[6],data[3]);
                        }
                        //plotbar
                        plotbar(data[2],data[3],data[4]);

                        $.unblockUI(); //跑完後關掉
                    },
                    error:function(){
                        console.log("error");
                        $.unblockUI(); //Loading...跑完後關掉
                    },
                    });
            };
        })

        $('#select_data_type').change(function (){
            $.blockUI({ css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff',
            message:"Loding..."
            } }); 

            var arr=[];
            $("[name=checkbox]:checkbox:checked").each(function(){
            arr.push($(this).val());
            });
            var arr_string = JSON.stringify(arr);
            //console.log(arr_string);
            //console.log(typeof(arr_string));//string
            var type = "Phalaenopsis";
            var select_data_type = $("#select_data_type").val(); 

            $.ajax({
                    url:'expression_profiling/ajax_parse3/',
                    data:{'data':arr_string,'type':type,'select_data_type':select_data_type},
                    type:'POST',
                    dataType:'json',
                    success:function(data){  
                        table_data = data;                        
                        
                        //plot_table
                        $('#mydiv').empty();
                        $('#mydiv').html("<table id='myDataTable'  class='cell-border table-striped'></table>");
                        create_table(data[2],data[3],data[4]);
                        //關閉ordering功能  
                        $('#myDataTable').DataTable({
                            "destroy": true,
                            "ordering":false,
                            "scrollX": true,
                            })

                        $('#checkall').click(function(){
                        console.log("ok");
                        if($('#checkall').prop("checked"))//如果全選按鈕有被選擇的話（被選擇是true）
                          {
                            //console.log("checkbox is checked");
                           //$("input[name='ID']").prop("checked",true);//把所有的核取方框的property都變成勾選
                           $('#myDataTable').DataTable()
                                .column(0)
                                .nodes()
                                .to$()
                                .find('input[name=ID]')
                                .prop('checked', this.checked);//true
                          }
                        else
                          {
                           //$("input[name='ID']").prop("checked",false);//把所有的核取方框的property都取消勾選
                           $('#myDataTable').DataTable()
                                .column(0)
                                .nodes()
                                .to$()
                                .find('input[name=ID]')
                                .prop('checked', false);
                          }
                        });
                        //plotheatmap
                        plotheatmap(data[2],data[3],data[4]); 
                         
                         //plotcluster
                        if (data[5]=="no picture"){
                            document.getElementById("img").src="";
                            $("#img_table").hide();
                            $("#cluster_text").html("<b>Because the Gene expression data have some null value,the Cluster chart can't be displayed!</b>");
                        }
                        else{
                            document.getElementById("img").src="../../../t50504_static/img/heatmap/" + data[5] + ".png" //絕對路徑寫法，因為寫相對路徑會出錯
                            //document.getElementById("img").src="{% static 'img/heatmap/OktRM.png' %}"
                        }

                        //plotpca
                        if (data[6]=="no pca"){
                            $("#pca").empty();
                            $("#pca").html("<b>Because the Gene expression data have some null value or the Gene expression data only have one column,the PCA chart can't be displayed!</b>");
                        }
                        else{
                            plotpca(data[6],data[3]);
                        }
                        //plotbar
                        plotbar(data[2],data[3],data[4]);
                        $.unblockUI(); //Loading...跑完後關掉
                    },
                    error:function(){
                        console.log("error");
                        $.unblockUI(); //Loading...跑完後關掉
                    },
                    });                 
             });

        
        $("#select").click(function(){        
            //不知道為什麼Ajax回傳的table_data會受下面的function或變數影響而改變，table_data資料中的"null"被改成了"-1"，所以這裡要在轉一次
            for (var i = 0, l = table_data[4].length; i < l; i++) {
                for (var j = 0, k = table_data[4][i].length; j < k; j++) {
                    if (table_data[4][i][j] == "-1") {
                        table_data[4][i].splice(j, 1, 'null')
                    }
                }
            };

            var checked_geneid2 = [];
            var checked_header = [];
            $("input[name = 'header']:checked").each(function (i) {
                var tmp = $(this).attr("id");
                checked_header.push(tmp);
                
            });
            /*$("input[name = 'ID']:checked").each(function (j) {
                var tmp2 = $(this).attr("id");
                checked_geneid2.push(tmp2);
            });*/
            $('#myDataTable').DataTable().column(0).nodes().to$().find('input[type="checkbox"]:checked').each(function(){
                //console.log($(this).val());
                checked_geneid2.push($(this).attr("id"));
            })

            if (checked_header.length==0||checked_geneid2.length==0){
                alert("Please check the gene ID checkbox and the organ checkbox!");
            }
            else{
                //防呆
                $("#select").attr("disabled","false");
                $("#reset").removeAttr('disabled');
                //console.log(checked_header);
                //console.log(checked_geneid2);
                //plot_table
                $('#mydiv').empty();
                $('#mydiv').html("<table id='myDataTable'  class='cell-border table-striped'></table>");

                obj = select_table(table_data[2],table_data[3],table_data[4],checked_header,checked_geneid2);
                $('#myDataTable').DataTable({
                    "destroy": true,
                    "scrollX": true,
                    })
                var select_header_string = JSON.stringify(obj.select_header);
                var select_geneid_string = JSON.stringify(obj.select_geneid);
                var select_body_string = JSON.stringify(obj.select_body);
                //console.log(select_header_string);
                //console.log(select_geneid_string);
                //console.log(select_body_string);
                $.ajax({
                    url:'expression_profiling/ajax_parse4/',
                    data:{'select_header':select_header_string,'select_geneid':select_geneid_string,'select_body':select_body_string},
                    type:'POST',
                    dataType:'json',
                    success:function(data){
                        //console.log(data);
                        //plotheatmap
                        plotheatmap(obj.select_header,obj.select_geneid,obj.select_body);  
                        //plotcluster
                        if (data[5]=="no picture"){
                            document.getElementById("img").src="";
                            $("#img_table").hide();
                            $("#cluster_text").html("<b>Because the Gene expression data have some null value,the Cluster chart can't be displayed!</b>");
                        }
                        else{
                        document.getElementById("img").src="../../../t50504_static/img/heatmap/" + data[0] + ".png" //絕對路徑寫法，因為寫相對路徑會出錯
                        //document.getElementById("img").src="{% static 'img/heatmap/OktRM.png' %}"
                        }

                        //plotpca
                        if (data[6]=="no pca"){
                            $("#pca").empty();
                            $("#pca").html("<b>Because the Gene expression data have some null value or the Gene expression data only have one column,the PCA chart can't be displayed!</b>");
                        }
                        else{
                            plotpca(data[1],obj.select_geneid);
                        }

                        //plotbar
                        plotbar(obj.select_header,obj.select_geneid,obj.select_body);                            
                    },
                    error:function(){
                        console.log("error");
                    },
                })
            }
        })

        $("#reset").click(function(){
            //防呆
            $("#reset").attr("disabled","false");
            $("#select").removeAttr('disabled');
            

            $.blockUI({ css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff',
            message:"Loding..."
            } });

            //不知道為什麼Ajax回傳的table_data會受下面的function或變數影響而改變，table_data資料中的"null"被改成了"-1"，所以這裡要在轉一次
            for (var i = 0, l = table_data[4].length; i < l; i++) {
                for (var j = 0, k = table_data[4][i].length; j < k; j++) {
                    if (table_data[4][i][j] == "-1") {
                        table_data[4][i].splice(j, 1, 'null')
                    }
                }
            };
            obj=""
            //plot_table
            $('#mydiv').empty();
            $('#mydiv').html("<table id='myDataTable'  class='cell-border table-striped'></table>");
            create_table(table_data[2],table_data[3],table_data[4]);
            //關閉ordering功能  
            $('#myDataTable').DataTable({
                "destroy": true,
                "ordering":false,
                "scrollX": true,
                })

            $('#checkall').click(function(){
            //console.log("ok");
            if($('#checkall').prop("checked"))//如果全選按鈕有被選擇的話（被選擇是true）
              {
                //console.log("checkbox is checked");
               $("input[name='ID']").prop("checked",true);//把所有的核取方框的property都變成勾選
              }
            else
              {
               $("input[name='ID']").prop("checked",false);//把所有的核取方框的property都取消勾選
              }
            });
            //plotheatmap
            plotheatmap(table_data[2],table_data[3],table_data[4]);  

            //plotcluster
            if (table_data[5]=="no picture"){
                document.getElementById("img").src="";
                $("#img_table").hide();
                $("#cluster_text").html("<b>Because the Gene expression data have some null value,the Cluster chart can't be displayed!</b>");
            }
            else{
                document.getElementById("img").src="../../../t50504_static/img/heatmap/" + table_data[5] + ".png" //絕對路徑寫法，因為寫相對路徑會出錯
                //document.getElementById("img").src="{% static 'img/heatmap/OktRM.png' %}"
            }

            //plotpca
            if (table_data[6]=="no pca"){
                $("#pca").empty();
                $("#pca").html("<b>Because the Gene expression data have some null value or the Gene expression data only have one column,the PCA chart can't be displayed!</b>");
            }
            else{
                plotpca(table_data[6],table_data[3]);
            }

            //plotbar
            plotbar(table_data[2],table_data[3],table_data[4]); 

            $.unblockUI(); //跑完後關掉            
        })

    $("#plot_cluster").click(function(){
        if ($("#colorbar").val()=="default"){
            var vmin ="default";
            var vmax ="default";     
            var figsize =$("#figsize").val();
            var row_cluster=$("#row_cluster").val();
            var cbar_pos=$("#cbar_pos").val();
            var cmap=$("#cmap").val();
            console.log(obj);
            if (obj==""){
                var cluster_body = table_data[4];
                var cluster_head = table_data[2];
                var cluster_geneid = table_data[3];
            }
            else{
                var cluster_body = obj.select_body;
                var cluster_head = obj.select_header;
                var cluster_geneid = table_data[3]; 
            }
             $.ajax({
                    url:'expression_profiling/ajax_parse5/',
                    data:{'cluster_body':JSON.stringify(cluster_body),'cluster_head':JSON.stringify(cluster_head),'cluster_geneid':JSON.stringify(cluster_geneid),'vmin':vmin,'vmax':vmax,'figsize':figsize,'row_cluster':row_cluster,'cbar_pos':cbar_pos,'cmap':cmap},
                    type:'POST',
                    dataType:'json',
                    success:function(data){
                        console.log(data);
                        
                        //plotcluster
                        if (data.pic_name=="no picture"){
                            document.getElementById("img").src="";
                        }
                        else{
                            document.getElementById("img").src="../../../t50504_static/img/heatmap/" + data.pic_name + ".png" //絕對路徑寫法，因為寫相對路徑會出錯
                            //document.getElementById("img").src="{% static 'img/heatmap/OktRM.png' %}"
                        }                           
                    },
                    error:function(){
                        console.log("error");
                    },
                })
        }
        else{
            var vmin =$("#vmin").val();
            var vmax = $("#vmax").val();
            var figsize =$("#figsize").val();
            var row_cluster=$("#row_cluster").val();
            var cbar_pos=$("#cbar_pos").val();
            var cmap=$("#cmap").val();
            if (vmax==""|| !(/(^[1-9]\d*$)/.test(vmax))){
                alert("Please query a positive number");
            }
            else{
                console.log(obj);
                if (obj==""){
                var cluster_body = table_data[4];
                var cluster_head = table_data[2];
                var cluster_geneid = table_data[3];
                }
                else{
                    var cluster_body = obj.select_body;
                    var cluster_head = obj.select_header;
                    var cluster_geneid = table_data[3]; 
                }
                $.ajax({
                    url:'expression_profiling/ajax_parse5/',
                    data:{'cluster_body':JSON.stringify(cluster_body),'cluster_head':JSON.stringify(cluster_head),'cluster_geneid':JSON.stringify(cluster_geneid),'vmin':vmin,'vmax':vmax,'figsize':figsize,'row_cluster':row_cluster,'cbar_pos':cbar_pos,'cmap':cmap},
                    type:'POST',
                    dataType:'json',
                    success:function(data){
                        console.log(data);
                        
                        //plotcluster
                        if (data.pic_name=="no picture"){
                            document.getElementById("img").src="";
                        }
                        else{
                            document.getElementById("img").src="../../../t50504_static/img/heatmap/" + data.pic_name + ".png" //絕對路徑寫法，因為寫相對路徑會出錯
                            //document.getElementById("img").src="{% static 'img/heatmap/OktRM.png' %}"
                        }                           
                    },
                    error:function(){
                        console.log("error");
                    },
                })
            }
        }
    })

    $("#colorbar").change(function(){
        if ($("#colorbar").val()=="default"){ 
            $("#vmin").attr("disabled","false");
            $("#vmax").attr("disabled","false");
        }
        else{
            $("#vmin").removeAttr('disabled');
            $("#vmax").removeAttr('disabled');
        }
    })

    $("#blast_result").click(function(){
        $("#resultlabel").show();            
        $("#mydiv").hide();
        $("#heatmap").hide();
        $("#bar").hide();
        $("#pca").hide();
        $("#img_div").hide();
        $("#ShowExpressionProfile").show();
        $("#select_data_type").hide();
        $("#select_button").hide();
        
     }) 
    $("#GeneExpression").click(function(){
        $("#resultlabel").hide();
        $("#mydiv").show();
        $("#heatmap").hide();
        $("#bar").hide();
        $("#pca").hide();
        $("#img_div").hide();
        $("#ShowExpressionProfile").hide();
        $("#select_data_type").show();
        $("#select_button").show();
        
     }) 
    $("#Heatmap").click(function(){
        $("#resultlabel").hide();
        $("#mydiv").hide();
        $("#heatmap").show();
        $("#bar").hide();
        $("#pca").hide();
        $("#img_div").hide();
        $("#ShowExpressionProfile").hide();
        $("#select_data_type").hide();
        $("#select_button").hide();
        
     })
    $("#Expressionpattern").click(function(){
        $("#resultlabel").hide();
        $("#mydiv").hide();
        $("#heatmap").hide();
        $("#bar").show();
        $("#pca").hide();
        $("#img_div").hide();
        $("#ShowExpressionProfile").hide();
        $("#select_data_type").hide();
        $("#select_button").hide();
        
     })
    $("#PCA").click(function(){
        $("#resultlabel").hide();
        $("#mydiv").hide();
        $("#heatmap").hide();
        $("#bar").hide();
        $("#pca").show();
        $("#img_div").hide();
        $("#ShowExpressionProfile").hide();
        $("#select_data_type").hide();
        $("#select_button").hide();
        
     })  
    $("#Cluster").click(function(){
        $("#resultlabel").hide();
        $("#mydiv").hide();
        $("#heatmap").hide();
        $("#bar").hide();
        $("#pca").hide();
        $("#img_div").show();
        $("#ShowExpressionProfile").hide();
        $("#select_data_type").hide();
        $("#select_button").hide();
        
     })               

    })
})

function create_blast_table(id_list,score_list,evalue_list,identities_list,positives_list,gaps_list,detail_list) {

            $("#mytable").append(string);
            var string = "";
            var shorthand = {"Peq":"Phalaenopsis","Dca":"Dendrobium","Apo":"Apostasia","Vpo":"Vpompona","Vsh":"Vshenzhenica","Pgu":"Pguangdongensis","Pzi":"Pzijinensis"}


            //add header
            string += "<thead class='thead-dark'><tr><th><input type='checkbox' id='CheckAll'>Check All ID</th><th>Query</th><th>Score</th><th>Expect</th><th>Identities</th><th>Positives</th><th>Gaps</th><th>Query detail</th></tr></thead>";
            $("#mytable").append(string);

            //add body
            $("#mytable").append("<tbody id=tb1>");
            //console.log(id_list.length);
            var string2 = "";
            for (var i = 0; i < id_list.length; i++) {
            //<a href=\"" + "http://cosbi.ee.ncku.edu.tw/t50504_project/GeneAnnotation/?id="+ lines[i][0:9] +"&type="+ Type + "\"  target=\"_blank\">" + lines[i][0:9] + "</a>"
                string2 += "<tr name ='tr" + i + "'><td><input type='checkbox' name='checkbox' value='"+ id_list[i] +"'></td><td><a href='http://cosbi.ee.ncku.edu.tw/t50504_project/GeneAnnotation/?id=" + id_list[i] +"&type="+ shorthand[id_list[i].substr(0,3)] +"' target='_blank'>"+ id_list[i] + "</a></td>"+"<td>" + score_list[i] + "</td>"+"<td>" + evalue_list[i] + "</td>"+"<td>" + identities_list[i] + "</td>"+"<td>" + positives_list[i] + "</td>"+"<td>" + gaps_list[i] + "</td><td><input type='button' value='view detail' class='view_detail'><div style='display: none;'><pre>" + detail_list[i] + "</pre></div></td></tr>";
            }
            $("#mytable").append(string2);
           
            $("#mytable").append("</tbody>");
            

        }

        
        function create_table(header,id,body) {
            //$("#myDataTable").empty();
            //console.log(inf);
            var string = "";
            //add header
            string += "<thead><tr><th><input type=checkbox id='checkall' name=CheckAll ID ><label for='CheckAll ID'> CheckAll ID</label></th>";
            for (var j = 0; j < header.length; j++) {
                string += "<th><input type=checkbox id='" + header[j] + "' name=header >" + header[j] + "</th>";
            }
            string += "</tr></thead>";
            $("#myDataTable").append(string);

            //add body
            $("#myDataTable").append("<tbody id=tb1>");
            //console.log("ok");
            //console.log(Object.keys(inf).length - 2);


            for (var i = 0; i < id.length; i++) {
                var string2 = "";
                string2 += "<tr name ='tr" + i + "'><td><input type=checkbox id='" + id[i] + "' name=ID >" + id[i] + "</td>";
            //console.log(inf[i + 2].length);
                for (var k = 0, l = body[i].length; k < l; k++) {
                 //console.log(inf[i + 2][k]);
                    string2 += "<td>" + body[i][k] + "</td>";
                 //console.log(string2);
                }
                string2 += "</tr>";
            //console.log(string2);
                $("#myDataTable").append(string2);
            }
            $("#myDataTable").append("</tbody>");
            $('#myDataTable').DataTable();

        }

        function select_table(header,geneid,body,checkedheader, checkedID) {
            var header = header
            var id = geneid;
            var header_dic = {};
            var id_dic = {};
            var select_header = [] ;
            var select_geneid = [];
            var select_body = [];

            for (var i = 0; i < header.length; i++) {
                header_dic[header[i]] = i;
            }
            for (var i = 0; i < id.length; i++) {
                id_dic[id[i]] = i;
            }

            $("#myDataTable").empty();
            var string = "";
            //add header
            string += "<thead><tr><th></th>";
            for (var j = 0; j < checkedheader.length; j++) {
                string += "<th>" + header[header_dic[checkedheader[j]]] + "</th>";
                select_header.push(checkedheader[j]);
                //console.log(select_header);
            }
            string += "</tr></thead>";
            $("#myDataTable").append(string);

            //add body
            $("#myDataTable").append("<tbody id=tb1>");

            for (var i = 0; i < checkedID.length; i++) {
                var temp = [];
                var string2 = "";
                string2 += "<tr name ='tr" + i + "'><td>" + id[id_dic[checkedID[i]]] + "</td>";
                for (var j = 0; j < checkedheader.length; j++) {
                    string2 += "<td>" + body[id_dic[checkedID[i]]][header_dic[checkedheader[j]]] + "</td>";
                    temp.push(body[id_dic[checkedID[i]]][header_dic[checkedheader[j]]]);
                }
                string2 += "</tr>";
                //console.log(string2);
                $("#myDataTable").append(string2);
                select_geneid.push(checkedID[i]);
                select_body.push(temp);
            }
            $("#myDataTable").append("</tbody>");
            $('#myDataTable').DataTable();
            //console.log(data);
            //console.log(select_header);
            //console.log(select_geneid);
            //console.log(select_body);
            return {'select_header':select_header,'select_geneid':select_geneid,'select_body':select_body};
        }

       
     function plotheatmap(header,id,body) {
         var xValues = header;
         var yValues = id.reverse();
         var zValues = body.reverse();
         //find max zValues
         var maxRow = zValues.map(function(row){ return Math.max.apply(Math, row); });
         console.log("各基因最大值:"+maxRow);
         var max = Math.max.apply(null, maxRow);
         //console.log(max);
         //find average
         var total = 0;
         for(var i = 0; i < maxRow.length; i++) {
            total += maxRow[i];
         }
         var avg = total / maxRow.length;
         console.log("平均最大值:"+avg);

         var data = [
       {
           z: zValues,
           x: xValues,
           y: yValues,
           colorscale: 'Hot',
           type: 'heatmap',
           "reversescale": true,//顏色反向
       }
         ];

         var layout = {
              title: 'Heatmap',
              annotations: [],
              xaxis: {
                ticks: '',
                side: 'top'
              }
          }

          for ( var i = 0; i < yValues.length; i++ ) {
              for ( var j = 0; j < xValues.length; j++ ) {
                var currentValue = zValues[i][j];
                if (currentValue > (max/2)) {
                  var textColor = 'white';
                }else{
                  var textColor = 'black';
                }
                var result = {
                  xref: 'x1',
                  yref: 'y1',
                  x: xValues[j],
                  y: yValues[i],
                  text: zValues[i][j],
                  font: {
                    family: 'Arial',
                    size: 12,
                    color: 'rgb(50, 171, 96)'
                  },
                  showarrow: false,
                  font: {
                    color: textColor
                  }
                };
                layout.annotations.push(result);
              }
            }



         Plotly.newPlot('heatmap', data,layout);
     }

        function plotpca(pca_list, geneid) {

            var listx = [];
            var listy = [];
            var textlist = geneid;

            for (var i = 0; i < Object.keys(pca_list).length; i++) {
                listx.push(pca_list[i][0]);
                listy.push(pca_list[i][1]);
            }

            var trace1 = {
                x: listx,
                y: listy,
                //x: [1, 2, 3, 4],
                //y: [10, 15, 13, 17],
                mode: 'markers',
                type: 'scatter',
                text: textlist
            };

            var data = [trace1];

            Plotly.newPlot('pca', data);
        }

        function plotbar(header,geneid,body) {
            var data = [];
            //var k = 'trace';
            for (var i = 0, l = Object.keys(body).length; i < l; i++) {
                for (var j = 0, k = body[i].length; j < k; j++) {
                    if (body[i][j] == "null") {
                        body[i].splice(j, 1, '-1');
                    };
                };
                //console.log(inf[i + 2]);
                window['trace' + i] = {
                                    x: header,
                                    y: body[i],
                                    name: geneid[i],
                                    type: 'bar'
                                    };
                data.push(window['trace' + i]);
            }
            //console.log(data);


            var layout = {
                yaxis: { title: 'FPKM' },
                barmode: 'group'
            };

            Plotly.newPlot('bar', data, layout);
        }