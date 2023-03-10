$(function(){})
$.ajaxSetup({
	data: {
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
});

$(document).ready(function() {


	
	$( ".table00" ).DataTable({
		"bPaginate": false, // 顯示換頁
		"searching": false, // 顯示搜尋
		"info":	false, // 顯示資訊
		'fixedHeader':true,
		stateSave: true,
	});
	$( ".table01" ).DataTable({
		"bPaginate": false, // 顯示換頁
		"searching": true, // 顯示搜尋
		"info":	false, // 顯示資訊
		'fixedHeader':true,
		stateSave: true,
	});
	var dt = $( ".intertable" ).DataTable({
		"order": [[ 7, "desc" ]],
		
		"bPaginate": false, // 顯示換頁
		"searching": true, // 顯示搜尋
		"info":	false, // 顯示資訊
		stateSave: true,
	});
	$( ".table1" ).DataTable({
		"bPaginate": true, // 顯示換頁
		"searching": true, // 顯示搜尋
		"info":	false, // 顯示資訊
		'fixedHeader':true,
		stateSave: true,
	});
	$( ".table3" ).DataTable({
		
		"bPaginate": true, // 顯示換頁
		"searching": true, // 顯示搜尋
		"info":	false, // 顯示資訊
		stateSave: true,
	});
	$("#result1").click(function(){
						
	
		$("#Set1").toggle();
		$("#Set1")[0].scrollIntoView();
		});
	$("#result12").click(function(){
		$("#Set32").toggle();
		$("#Set32")[0].scrollIntoView();
			});
	$("#result2").click(function(){

		$("#Set3").toggle();
		$("#Set3")[0].scrollIntoView();
		});
	$("#result3").click(function(){
		$("#Set4").toggle();
		$("#Set4")[0].scrollIntoView();
		});
	$("#Fbtn").click(function(){
			$("#Fs").toggle();
			});	
	//定量按了跳到圖的地方
	//var qua_list=['mw','te','rd_ing1_ing1','rd_ger1_ger1','rd_mcm1_mcm1','rd_sub1_sub1','expressionlevel','halflife','transcriptionalfreq']
	$("#mw").click(function(){
		$("#PIC1").toggle();
		$("#PIC1")[0].scrollIntoView();
	});
	$("#te").click(function(){
		$("#PIC2").toggle();
		$("#PIC2")[0].scrollIntoView();
	});
	$("#rd_ing1_ing1").click(function(){
		$("#PIC3").toggle();
		$("#PIC3")[0].scrollIntoView();
	});
	$("#rd_ger1_ger1").click(function(){
		$("#PIC4").toggle();
		$("#PIC4")[0].scrollIntoView();
	});
	$("#rd_mcm1_mcm1").click(function(){
		$("#PIC5").toggle();
		$("#PIC5")[0].scrollIntoView();
	});
	$("#rd_sub1_sub1").click(function(){
		$("#PIC6").toggle();
		$("#PIC6")[0].scrollIntoView();
	});
	$("#expressionlevel").click(function(){
		$("#PIC7").toggle();
		$("#PIC7")[0].scrollIntoView();
	});
	$("#halflife").click(function(){
		$("#PIC8").toggle();
		$("#PIC8")[0].scrollIntoView();
	});
	$("#transcriptionalfreq").click(function(){
		$("#PIC9").toggle();
		$("#PIC9")[0].scrollIntoView();
	});
	//var result_list = ['F294','F183','FKEGG']
	var ids1 = $('.ajax_jqP').map(function(){
		return this.id;
	}).get();
	//改成用for迴圈創建$.click selector
	$(".ajax_jqP").each(function(index) {
		$("#"+ids1[index]).on('click',function() {

			$('#showdata1_pop').empty()
			$('#shadow').css('display','block')
			$('#showdata1_pop').css('display','block')
			$.ajax({
				url: "/ajax_jqP/",
				data: {
					'keyname':$('#'+ids1[index]).attr('name')
				},
				success: function(data) {
					$('#showdata1_pop').append("<table class='pop1' border='1'><thead><th width='40%'>Gene ID</th><th colspan='1' width='15%'>Input1 Genes</th><th width='15%'>Input2 Intersects</th> </thead><tbody id='tb_pop1'></tbody> </table>")
					//返回值 data 在這裡是一個列表
					for (var i in data) {
						// 把 data 的每一項顯示在網頁上
						$('#tb_pop1').append("<tr><td width='40%' align='center'><a href=https://www.yeastgenome.org/locus/"+i+"  target='_blank'>"+i+"</a></td>"+
						"<td width='15%' align='center'>"+data[i][0]+"</td>"+
						"<td width='15%' align='center'>"+data[i][1]+"</td></tr>");
					}
					$( ".pop1" ).DataTable({
					
						"bPaginate": false, // 顯示換頁
						"searching": true, // 顯示搜尋
						"info":	false, // 顯示資訊
						stateSave: true,
					});
				},
				type: "POST",
				dataType: "json"
			});

		});
	});
	var ids = $('.ajax_jqP_2').map(function(){
		return this.id;
	}).get();
	
	$(".ajax_jqP_2").each(function(index) {
		dt.on('click','#'+ids[index],function(){
			$('#showdata1_pop').empty()
			$('#shadow').css('display','block')
			$('#showdata1_pop').css('display','block')
	
			//
			$.ajax({
				url: "/ajax_jqP2/",
				data: {
					'keyname2':$('#'+ids[index]).attr('name')
				},
				success: function(data) {
					$('#showdata1_pop').append("<table class='pop1' border='1'><thead><th width='40%'>Gene ID</th><th width='15%'>symbol</th><th width='15%'>Experimental system</th><th width='15%'>Author</th> <th width='15%'>pubmedID</th><th width='15%'>Throughout</th></thead><tbody id='tb_pop1'></tbody> </table>")
					//返回值 data 在這裡是一個列表
					for (var i in data) {
						// 把 data 的每一項顯示在網頁上
						$('#tb_pop1').append("<tr><td width='40%' align='center'>"+i+"</td>"+
						"<td width='15%' align='center'>"+data[i][0]+"</td>"+
						"<td width='15%' align='center'>"+data[i][1]+"</td>"+
						"<td width='15%' align='center'>"+data[i][2]+"</td>"+
						"<td width='15%' align='center'> <a href=https://www.ncbi.nlm.nih.gov/pubmed/"+data[i][3]+" target='_blank'>"+data[i][3]+"</a></td>"+
						"<td width='15%' align='center'>"+data[i][4]+"</td></tr>");
					}
					$( ".pop1" ).DataTable({
						
						"bPaginate": false, // 顯示換頁
						"searching": true, // 顯示搜尋
						
						"info":	false, // 顯示資訊
						stateSave: true,
					});
				},
				type: "POST",
				dataType: "json"
			});
		})
	})
		//
	
	//deal pop up
	$("#shadow").click(function(){
			$("#shadow").css('display','none');
			$('#showdata1_pop').css('display','none')
		});


});
//deal pop out window

//
var textarea = document.getElementById('textar');
var Selectgene = document.getElementById('group1')
var singleinputBOX = document.getElementById('single')
var doubleinputBOX = document.getElementById('double')
var tog3 = document.getElementById('Set4')
var tog2 = document.getElementById('Set3')
var tog22=document.getElementById('Set32')
var tog1 = document.getElementById('Set1')

var togpic1=document.getElementById('PIC1')
var togpic2=document.getElementById('PIC2')
var togpic3=document.getElementById('PIC3')
var togpic4=document.getElementById('PIC4')
var togpic5=document.getElementById('PIC5')
var togpic6=document.getElementById('PIC6')
var togpic7=document.getElementById('PIC7')
var togpic8=document.getElementById('PIC8')
var togpic9=document.getElementById('PIC9')
var k = 0
var m = 0
var cutoff = document.getElementById('cutoff')

Selectgene.style.display='none';
cutoff.style.display='none';
tog1.style.display='none';
tog2.style.display='none';
tog22.style.display='none';
tog3.style.display='none';
togpic1.style.display='none';
togpic2.style.display='none';
togpic3.style.display='none';
togpic4.style.display='none';
togpic5.style.display='none';
togpic6.style.display='none';
togpic7.style.display='none';
togpic8.style.display='none';
togpic9.style.display='none';
function ck(obj){
	if(obj.checked){
		textarea.style.display='none';
		Selectgene.style.display='flex';
		if( m==1 ){
			doubleinputBOX.checked = false;
		}
		}
	else{
		textarea.style.display='inline';
		Selectgene.style.display='none';
		}
	return k = 1	
	}
function ckD(obj){   //CUTOFF POP UP
		if(obj.checked){
			cutoff.style.display='inline';
			}
		else{
			cutoff.style.display='none';
			}

		}	
function ck2(){
		textarea.disabled=false;	
	}	
function ClearTextArea(obj)
{	
	if(obj.checked){
		textarea.style.display='inline';
		Selectgene.style.display='none';
		if (k == 1) {
			singleinputBOX.checked = false;
		}
	}
	return m = 1 
}

function showExample(i){
	if(i==1)
	{
		$('#text1').val("YDR258C\nYKR091W\nYEL011W\nYPL171C\nYOR027W\nYDR453C\nYIL154C\nYGR223C\nYCR021C\nYGR250C\nYNL160W\nYHR008C\nYJR104C\nYBR151W\nYOL151W\nYHR097C\nYER101C\nYOR136W\nYLR346C\nYDR353W\nYJL001W\nYDL029W\nYIL077C\nYPR167C\nYDR229W\nYOL116W\nYFR024C-A\nYLR345W\nYML042W\nYOL048C\nYGR256W\nYGL108C\nYDR423C\nYBR046C\nYBR255W\nYDR513W\nYGR080W\nYPR047W\nYDL124W\nYNL156C\nYFL016C\nYER059W\nYBR126C\nYBL050W\nYPR067W\nYFL030W\nYLL029W\nYBR137W\nYOR274W\nYLR109W\nYPR108W\nYJR019C\nYDR533C\nYPL203W\nYDR001C\nYBL041W\nYIL042C\nYGR193C\nYGL157W\nYLL060C\nYKL087C\nYMR210W\nYJL048C\nYML131W\nYDR059C\nYKL071W\nYER053C\nYPR127W\nYDR003W\nYKL195W\nYMR318C\nYNL241C\nYLL056C\nYGL090W\nYDR368W\nYBR119W\nYDL243C\nYGR209C\nYGL181W\nYOL032W\nYPL091W\nYBL086C\nYDR005C\nYER079W\nYJL057C\nYJL155C\nYLR259C\nYBR241C\nYKR009C\nYPL095C\nYDR256C\nYGR112W\nYNL134C\nYGR248W\nYBL064C\nYKL145W\nYOL052C-A\nYMR090W\nYFR050C\nYGL011C\nYDL025C\nYAL039C\nYOR157C\nYGR237C\nYBR008C\nYLR369W\nYOL038W\nYMR041C\nYMR315W\nYHR016C\nYHR176W\nYKL086W\nYNL202W\nYKR076W\nYPL215W\nYLL023C\nYLR460C\nYNL173C\nYOR259C\nYKL103C\nYKL051W\nYGR088W\nYCR102C\nYMR173W\nYGL037C\nYKR018C\nYGR130C\nYPL196W\nYLR205C\nYPL173W\nYMR222C\nYBR214W\nYBR177C\nYOL073C\nYMR174C\nYAL034C\nYJL036W\nYLR225C\nYHR132W-A\nYHR198C\nYNL037C\nYDL097C\nYKR066C\nYDL110C\nYDR516C\nYGL059W\nYNL239W\nYBR062C\nYDL057W\nYGL237C\nYOR358W\nYBR280C\nYPL166W\nYMR139W\nYPL087W\nYGR019W\nYCL035C\nYOR042W\nYOR352W\nYMR086W\nYGR002C\nYOR117W\nYIR039C\nYPL152W\nYGR136W\nYML129C\nYDR486C\nYMR226C\nYPL186C\nYIL113W\nYMR114C\nYKL150W\nYBL006C\nYCL040W\nYEL012W\nYBR223C\nYJR021C\nYKL067W\nYMR253C\nYEL052W\nYBR006W\nYDL204W\nYMR193W\nYDR171W\nYMR092C\nYJL171C\nYLR356W\nYGR008C\nYGL082W\nYKR011C\nYBR273C\nYJR062C\nYDR493W\nYLR216C\nYOR223W\nYBR262C\nYHR161C\nYHR195W\nYNR007C\nYLR206W\nYMR104C\nYNL214W\nYLL039C\nYBR149W\nYDL045C\nYER094C\nYLR251W\nYOR267C\nYCR009C\nYDR070C\nYMR311C\nYKL094W\nYLL006W\nYNL155W\nYBR109C\nYDL202W\nYDL099W\nYIL136W\nYNL100W\nYKL142W\nYGR231C\nYOL065C\nYDR204W\nYHL021C\nYHR030C\nYJL053W\nYOL083W\nYMR281W\nYJL066C\nYLR258W\nYLR064W\nYFR008W\nYKL095W\nYAR027W\nYFR053C\nYOR273C\nYHR106W\nYPL004C\nYGL053W\nYLR093C\nYOR181W\nYBR269C\nYOR023C\nYPL206C\nYEL005C\nYDR032C\nYOL096C\nYLR257W\nYBR108W\nYER130C\nYMR113W\nYDL126C\nYGR005C\nYDR391C\nYJR142W\nYIL097W\nYGL098W\nYNR001C\nYKL035W\nYAL061W\nYJR008W\nYFL056C\nYBL029C-A\nYBR199W\nYGR048W\nYFL044C\nYHR179W\nYGR194C\nYFL054C\nYGL047W\nYKL091C\nYDL216C\nYGR111W\nYML092C\nYDR129C\nYER093C-A\nYDR427W\nYDR532C\nYIR025W\nYER087W\nYJR052W\nYGL153W\nYBR169C\nYNL208W\nYGR052W\nYDR392W\nYOR020C\nYGR053C\nYML068W\nYIL098C\nYBR053C\nYBR054W\nYKL188C\nYER134C\nYIL033C\nYPL247C\nYDR246W\nYIR014W\nYGR268C\nYDL072C\nYMR110C\nYKL107W\nYEL050C\nYGR043C\nYBR173C\nYDR047W\nYML070W\nYDR358W\nYDL169C\nYMR251W-A\nYDR041W\nYPR103W\nYJL164C\nYML004C\nYKR049C\nYDR058C\nYBR014C\nYOR036W\nYHR104W\nYBR117C\nYMR197C\nYOR161C\nYGR017W\nYOR120W\nYML128C\nYGL134W\nYBR256C\nYDR313C\nYHR029C\nYLL026W\nYDR328C\nYER161C\nYFL042C\nYNL305C\nYKL064W\nYLR270W\nYOR022C\nYMR169C\nYAL012W\nYJR096W\nYMR105C\nYNL007C\nYPL191C\nYJL144W\nYOL043C\nYJL068C\nYDR031W\nYJL060W\nYMR028W\nYBR056W\nYFR017C\nYDR294C\nYKL193C\nYER067W\nYDR202C\nYJL141C\nYDL237W\nYLR297W\nYOR028C\nYNL260C\nYDR272W\nYPR107C\nYCL032W\nYLR164W\nYIR011C\nYDR479C\nYPR109W\nYJL115W\nYPR147C\nYHR004C\nYHR171W\nYMR004W\nYIR003W\nYMR297W\nYFR045W\nYIL117C\nYKL085W\nYDR265W\nYFL059W\nYIR024C\nYOR215C\nYBR170C\nYOR227W\nYDL078C\nYDL147W\nYER012W\nYCR036W\nYDR405W\nYHR012W\nYDL087C\nYIL157C\nYPR093C\nYDL218W\nYIL007C\nYHR147C\nYBR026C\nYNL077W\nYHR096C\nYIL101C\nYOL082W\nYBL056W\nYLR102C\nYOR220W\nYDR074W\nYIL029C\nYPR200C\nYBR193C\nYPL119C\nYNL231C\nYMR140W\nYMR314W\nYDL022W\nYKR014C\nYIR036C\nYFR041C\nYAR033W\nYGR076C\nYMR181C\nYLL055W\nYOL117W\nYKL213C\nYKL016C\nYDR287W\nYGL038C\nYDR477W\nYKL170W\nYFR052W\nYGL048C\nYOR292C\nYKL133C\nYDR054C\nYKL088W\nYMR027W\nYGL205W\nYMR284W\nYDR162C\nYBL091C-A\nYCL034W\nYBR179C\nYDL130W-A\nYML120C\nYER100W\nYIL074C\nYGL161C\nYMR067C\nYMR267W\nYOR007C\nYDL146W\nYDR322W\nYNL294C\nYNL181W\nYMR250W\nYPL014W\nYGR132C\nYLR168C\nYBR183W\nYHL034C\nYNL083W\nYPL003W\nYGR100W\nYJR100C\nYIL135C\nYBR204C\nYNR006W\nYKR007W\nYHR053C\nYLR439W\nYBL038W\nYLL058W\nYER020W\nYIL010W\nYGL004C\nYMR258C\nYGR207C\nYDL007W\nYJR010W\nYMR244C-A\nYHR200W\nYGL066W\nYDL168W\nYKL007W\nYKL098W\nYFR049W\nYIR038C\nYOL071W\nYBR035C\nYFR010W\nYKL013C\nYPL224C\nYCR076C\nYMR251W\nYNR068C\nYDL223C\nYGL104C\nYKR046C\nYHR002W\nYPL202C\nYLR387C\nYBR052C\nYLR136C\nYNL194C\nYHR028C\nYER152C\nYGR235C\nYOR173W\nYCR073W-A\nYDR387C\nYDR011W\nYNL092W\nYGR086C\nYBR272C\nYDL020C\nYAL008W\nYER143W\nYDR236C\nYDR494W\nYCL026C-A\nYNR032W\nYGR165W\nYGL185C\nYJL163C\nYPL262W\nYJL131C\nYIL034C\nYJR085C\nYER037W\nYHR190W\nYIL062C\nYDR022C\nYKL002W\nYJR059W\nYLR092W\nYNL234W\nYIL165C\nYLR149C\nYLR219W\nYFR014C\nYNL025C\nYDR330W\nYGR044C\nYIL087C\nYIR018W\nYBL043W\nYDR043C\nYLR178C\nYPR023C\nYDR214W\nYCL017C\nYML057W\nYDR394W\nYDR061W\nYPL084W\nYIL164C\nYJL161W\nYGR249W\nYPR079W\nYDR462W\nYGR023W\nYGL096W\nYIL045W\nYOL122C\nYIL116W\nYGR197C\nYGL045W\nYJL101C\nYOR226C\nYAL016W\nYCR019W\nYIL056W\nYGR142W\nYIL108W\nYOR362C\nYKR052C\nYAL031C\nYOL129W\nYDL106C\nYKL168C\nYDR480W\nYGL091C\nYMR038C\nYLR337C\nYNL312W\nYPR183W\nYKR069W\nYPR094W\nYLR213C\nYOL055C\nYNL195C\nYBL058W\nYGL196W\nYPR040W\nYPR131C\nYDL246C\nYOR285W\nYFR021W\nYKR071C\nYPL135W\nYPR008W\nYDR388W\nYHR199C\nYHL002W\nYLR163C\nYJL026W\nYBL015W\nYLR155C\nYBR107C\nYKL026C\nYMR077C\nYPL100W\nYBL019W\nYMR085W\nYML069W\nYDR132C\nYAL060W\nYMR261C\nYJR051W\nYDR231C\nYKL157W\nYML086C\nYGL114W\nYPR184W\nYIL153W\nYKL100C\nYDL017W\nYPL229W\nYPL150W\nYGL025C\nYDR487C\nYJR065C\nYLR193C\nYNL274C\nYPR024W\nYJR048W\nYOR019W\nYML117W\nYGL058W\nYJL082W\nYOR386W\nYNR034W\nYKL040C\nYJL046W\nYHR048W\nYKL162C\nYNL322C\nYJR125C\nYLR429W\nYDR515W\nYCR030C\nYDR304C\nYHL019C\nYDR276C\nYOR298C-A\nYDR255C\nYHR113W\nYHR001W\nYER175C\nYBR176W\nYGL039W\nYNR035C\nYDR100W\nYML007W\nYDR244W\nYDL115C\nYHL036W\nYNL284C\nYGL252C\nYOR257W\nYBR016W\nYPL002C\nYFR004W\nYOR052C\nYLR248W\nYDR525W-A\nYPL230W\nYDL161W\nYHR192W\nYNR069C\nYAL014C\nYBR234C\nYML087C\nYPL151C\nYLR108C\nYPR065W\nYDL002C\nYDR517W\nYOL100W\nYER038C\nYDL199C\nYBL080C\nYDL142C\nYDL113C\nYPR149W\nYMR031C\nYDR035W\nYEL056W\nYBL033C\nYDL230W\nYER116C\nYAL009W\nYGL150C\nYMR265C\nYPL059W\nYLL018C-A\nYKL052C\nYLL019C\nYAL063C\nYHL048W\nYDR222W\nYDL128W\nYDL183C\nYGR247W\nYER035W\nYEL060C\nYHR038W\nYGR021W\nYPL249C\nYPL214C\nYGR006W\nYBL091C\nYFL027C\nYDR350C\nYOL111C\nYLR220W\nYPL154C\nYGL087C\nYFL029C\nYPR042C\nYGR013W\nYCL051W\nYLR290C\nYIR035C\nYDR539W\nYBR071W\nYKL059C\nYGR101W\nYKR061W\nYDR511W\nYDR306C\nYDL024C\nYJR084W\nYIL041W\nYLR133W\nYHR114W\nYLR299W\nYMR276W\nYJL024C\nYML130C\nYDR237W\nYOR059C\nYCL008C\nYIL114C\nYFR003C\nYML025C\nYDR475C\nYHR017W\nYGL002W\nYPR081C\nYCL033C\nYMR134W\nYPL015C\nYML100W\nYCR011C\nYMR037C\nYBL021C\nYOR280C\nYKR067W\nYML028W\nYEL039C\nYJL126W\nYHR140W\nYDL088C\nYML013W\nYJR091C\nYOR194C\nYIL013C\nYBR185C\nYJL100W\nYOL110W\nYNL097C\nYDR071C\nYPR061C\nYDL180W\nYDR135C\nYLR260W\nYGR058W\nYPR201W\nYMR166C\nYCR024C\nYMR157C\nYDR296W\nYGR010W\nYBR095C\nYLR312C\nYGR154C\nYDR066C\nYHR112C\nYPL159C\nYAL054C\nYAL055W\nYPL049C\nYCR004C\nYJR022W\nYKL163W\nYHR074W\nYDR512C\nYDR069C\nYJL128C\nYER062C\nYPR199C\nYAL048C\nYDL086W\nYLR047C\nYOL119C\nYLL051C\nYDR125C\nYJL063C\nYNL042W\nYIL172C\nYJL210W\nYEL057C\nYOR054C\nYER090W\nYIL120W\nYDL222C\nYDR262W\nYLR113W\nYDR463W\nYBR070C\nYPR158W\nYOR163W\nYFL010C\nYJL072C\nYDR055W\nYIR037W\nYBR147W\nYJR130C\nYJL170C\nYDL182W\nYPR005C\nYLR144C\nYLR390W\nYNR047W\nYOL013C\nYJL174W\nYHR189W\nYBR103W\nYLR218C\nYMR273C\nYER076C\nYGR239C\nYLR027C\nYER034W\nYHR111W\nYAL020C\nYIL160C\nYGL246C\nYOL027C\nYER093C\nYLR287C\nYDR207C\nYCL031C\nYPL267W\nYDR448W\nYML014W\nYFL036W\nYJL147C\nYLL022C\nYER151C\nYMR207C\nYER137C\nYMR269W\nYKR019C\nYPL069C\nYGR091W\nYBR188C\nYDR198C\nYKL203C\nYNL227C\nYLR086W\nYDR291W\nYJR141W\nYHR152W\nYGL107C\nYOR026W\nYMR190C\nYOR149C\nYDR052C\nYDR179C\nYGR199W\nYHR077C\nYCR016W\nYDR190C\nYER124C\nYGR099W\nYBL017C\nYHR187W\nYDR208W\nYGR056W\nYPL101W\nYKL082C\nYIL151C\nYJR129C\nYHR100C\nYDR013W\nYIL149C\nYER164W\nYOR166C\nYFL026W\nYNL207W\nYLR071C\nYOL022C\nYDL166C\nYGL176C\nYBR184W\nYAL026C\nYLR049C\nYLR096W\nYBL026W\nYBR246W\nYGL113W\nYNR011C\nYDL195W\nYHR098C\nYIR023W\nYML099C\nYDR143C\nYHR108W\nYKL176C\nYNL172W\nYPL041C\nYPR189W\nYDR123C\nYLR404W\nYGR083C\nYLR005W\nYDR240C\nYDR021W\nYML060W\nYOR287C\nYOR195W\nYER075C\nYPL235W\nYNL222W\nYFL048C\nYOR238W\nYOL093W\nYPR196W\nYGR024C\nYNL062C\nYNR048W\nYIL159W\nYLR183C\nYDR520C\nYNL047C\nYGR049W\nYJL029C\nYGL145W\nYLR182W\nYPL210C\nYDR238C\nYHL013C\nYOL031C\nYPL085W\nYGL169W\nYLR051C\nYIL031W\nYDR279W\nYOR378W\nYLR278C\nYBR291C\nYBL008W\nYDR489W\nYDR228C\nYGR271W\nYKL042W\nYJR013W\nYML072C\nYHL017W\nYGL236C\nYLR401C\nYGR089W\nYBR276C\nYDL226C\nYFL034W\nYAR035W\nYPR105C\nYIL004C\nYLR320W\nYGL064C\nYBR281C\nYOL146W\nYOR260W\nYDR459C\nYNL217W\nYGR148C\nYNL050C\nYDR217C\nYDL209C\nYOL141W\nYJL069C\nYMR061W\nYKR028W\nYGR166W\nYHR072W-A\nYOR188W\nYPR144C\nYNR063W\nYEL016C\nYLR424W\nYDL079C\nYHL039W\nYDR189W\nYOR106W\nYJR144W\nYML065W\nYGL256W\nYDR261C\nYOR001W\nYLR462W\nYOR087W\nYGL190C\nYDL058W\nYGL211W\nYDR020C\nYPL145C\nYNL287W\nYNL068C\nYDR331W\nYML031W\nYDR225W\nYOL149W\nYDL120W\nYAL046C\nYJR055W\nYHR023W\nYPL061W\nYJR007W\nYLR221C\nYPL047W\nYMR218C\nYLR042C\nYHR184W\nYOL123W\nYDR299W\nYOL078W\nYLL036C\nYNL327W\nYKL033W\nYLR138W\nYOL006C\nYDR326C\nYHR155W\nYDR499W\nYBR058C\nYDR390C\nYDR044W\nYJL110C\nYHR066W\nYLR007W\nYLR422W\nYDR174W\nYFL002C\nYLR274W\nYNL088W\nYLR318W\nYPL175W\nYIL127C\nYDR524C\nYIL103W\nYBR161W\nYHL003C\nYNL201C\nYBR210W\nYLR447C\nYLR335W\nYNL311C\nYOL003C\nYGL247W\nYOR349W\nYMR078C\nYPR083W\nYMR246W\nYDR312W\nYML082W\nYML108W\nYHR079C\nYPL266W\nYML103C\nYNR038W\nYOR271C\nYBL009W\nYAL029C\nYBL052C\nYOR283W\nYGR004W\nYER167W\nYGR093W\nYDR086C\nYDR297W\nYML096W\nYGR140W\nYDR211W\nYLR015W\nYGR094W\nYDL102W\nYPL116W\nYMR146C\nYER174C\nYLR020C\nYPL242C\nYCR093W\nYCL036W\nYBR086C\nYNL326C\nYDR159W\nYOR313C\nYMR144W\nYDR146C\nYML111W\nYOR151C\nYPR082C\nYHR120W\nYOL034W\nYIL126W\nYGR071C\nYGL238W\nYKL080W\nYGR063C\nYPL237W\nYLR399C\nYIL014W\nYBR297W\nYER171W\nYOR264W\nYPR141C\nYJL117W\nYKR044W\nYBR239C\nYBR010W\nYJR076C\nYBR154C\nYML006C\nYLL004W\nYLR228C\nYLL048C\nYIL020C\nYKL219W\nYOR101W\nYBR021W\nYNR028W\nYDR440W\nYLR197W\nYGR125W\nYPR122W\nYER111C\nYJR003C\nYLR210W\nYNL283C\nYLR242C\nYJL187C\nYPR095C\nYDR245W\nYPR163C\nYNL275W\nYHR204W\nYJL181W\nYKL185W\nYJR115W\nYER031C\nYLR438C-A\nYNL221C\nYOR154W\nYDR389W\nYGR117C\nYNL022C\nYDR349C\nYIL158W\nYNL145W\nYOR356W\nYBL014C\nYNL282W\nYNL255C\nYGL077C\nYML046W\nYBL003C\nYOR159C\nYOR144C\nYOR252W\nYBL031W\nYAL040C\nYLR442C\nYCL011C\nYNL211C\nYBL035C\nYNL280C\nYMR123W\nYIL018W\nYDL220C\nYDL073W\nYDR152W\nYDR365C\nYIL129C\nYMR076C\nYDR302W\nYJL209W\nYJL129C\nYOL142W\nYJL087C\nYOR093C\nYMR129W\nYER105C\nYDR449C\nYOR295W\nYDR367W\nYDL240W\nYNL113W\nYIL096C\nYAL019W\nYIL092W\nYCL045C\nYNL078W\nYKR025W\nYOR355W\nYHR035W\nYKL112W\nYNR016C\nYMR070W\nYBR192W\nYDR283C\nYLR091W\nYGR081C\nYDR372C\nYKL181W\nYDR150W\nYML106W\nYGR173W\nYDR496C\nYPR164W\nYJL118W\nYMR288W\nYPL029W\nYLR146C\nYKL125W\nYER046W\nYML104C\nYNL066W\nYNL204C\nYDL145C\nYKL212W\nYLR067C\nYCR008W\nYBR030W\nYOL138C\nYNL152W\nYNL139C\nYHL001W\nYBR002C\nYDR457W\nYGR014W\nYMR015C\nYNL044W\nYEL061C\nYOR034C\nYLR022C\nYLR068W\nYLR389C\nYNL188W\nYLR036C\nYKR008W\nYML061C\nYMR010W\nYNL096C\nYJL092W\nYKL166C\nYOR312C\nYDR465C\nYML077W\nYNL292W\nYGR128C\nYKL018W\nYKL172W\nYBR275C\nYOR212W\nYGL029W\nYKL015W\nYDR464W\nYPL265W\nYMR079W\nYML075C\nYNL031C\nYBL029W\nYOR168W\nYFL037W\nYNL085W\nYKR086W\nYMR215W\nYKL116C\nYDR239C\nYPR056W\nYER036C\nYJL091C\nYOR297C\nYLL032C\nYMR013C\nYBR073W\nYOR276W\nYGR198W\nYHR186C\nYGR082W\nYGR103W\nYBL106C\nYLR385C\nYDR111C\nYHR042W\nYPL184C\nYIL064W\nYNL316C\nYAR014C\nYOL021C\nYGR158C\nYKL154W\nYMR238W\nYMR243C\nYIL104C\nYBL104C\nYLL043W\nYCR094W\nYHR045W\nYFL067W\nYHR154W\nYDL148C\nYBR283C\nYLR057W\nYHR170W\nYLR106C\nYER056C\nYNL153C\nYML123C\nYMR048W\nYDL003W\nYOR078W\nYDR110W\nYDL141W\nYDR497C\nYDR333C\nYIL040W\nYLR105C\nYBR187W\nYCR051W\nYML056C\nYDR447C\nYDR395W\nYKL068W\nYLR186W\nYJR054W\nYIL083C\nYDR165W\nYNL058C\nYBR038W\nYKL048C\nYNL262W\nYBR271W\nYNR052C\nYER113C\nYDR419W\nYOR038C\nYJL010C\nYDL064W\nYGR187C\nYHR172W\nYOR326W\nYJL111W\nYHR205W\nYLR003C\nYNR018W\nYOR067C\nYKR094C\nYBL089W\nYJR112W\nYJR061W\nYLR343W\nYJR133W\nYDL093W\nYBL011W\nYGL116W\nYLR451W\nYGL144C\nYLR131C\nYLR227C\nYDR492W\nYMR126C\nYEL040W\nYLR018C\nYGL139W\nYMR299C\nYAL035W\nYBR029C\nYPR033C\nYEL076C-A\nYPR186C\nYLR406C\nYDR224C\nYBR265W\nYGR041W\nYOL019W\nYPR051W\nYGR175C\nYBR172C\nYOL015W\nYGL083W\nYOR044W\nYCL002C\nYLR291C\nYBR028C\nYOL077C\nYJL074C\nYDR089W\nYDR398W\nYPR052C\nYOR205C\nYBR143C\nYBL002W\nYBL034C\nYPL043W\nYDR191W\nYDR184C\nYBR142W\nYOR334W\nYMR239C\nYER132C\nYDL167C\nYLR443W\nYPL063W\nYDL171C\nYJL035C\nYDR234W\nYDR038C\nYDR450W\nYML024W\nYNL278W\nYGL070C\nYGR047C\nYEL001C\nYHR196W\nYJL039C\nYGL127C\nYJL157C\nYPR120C\nYMR036C\nYOR011W\nYPL081W\nYKR060W\nYMR270C\nYKL144C\nYOR246C\nYMR212C\nYHR165C\nYNL218W\nYLR432W\nYAL053W\nYDL155W\nYLR129W\nYER106W\nYJL194W\nYOR201C\nYGR188C\nYOR307C\nYJL168C\nYKL027W\nYNL126W\nYBR034C\nYNR053C\nYPL040C\nYGR030C\nYDR471W\nYGR098C\nYNL119W\nYLR430W\nYPL032C\nYLR305C\nYFL017C\nYJL019W\nYFL004W\nYPL125W\nYFL001W\nYLR321C\nYDL040C\nYPL068C\nYPL253C\nYDR075W\nYDR310C\nYOL095C\nYDR101C\nYGR032W\nYOL012C\nYLR413W\nYPL128C\nYJL033W\nYDR083W\nYIL109C\nYCR054C\nYBR112C\nYJR066W\nYDR194C\nYIL052C\nYGR116W\nYOL128C\nYEL029C\nYJR002W\nYGL224C\nYIL038C\nYOR305W\nYML019W\nYOR330C\nYBR158W\nYNL021W\nYDR325W\nYLR089C\nYBR004C\nYMR309C\nYML076C\nYOR296W\nYKL205W\nYJL011C\nYKL008C\nYOR016C\nYOR073W\nYOR233W\nYGL028C\nYIL130W\nYGL257C\nYLR008C\nYCR063W\nYPR143W\nYPR031W\nYPL115C\nYPL030W\nYLR407W\nYCR057C\nYLR063W\nYDR147W\nYMR014W\nYLR223C\nYER122C\nYJR016C\nYBL054W\nYEL048C\nYLR190W\nYLR256W\nYLR435W\nYML052W\nYHR206W\nYNL132W\nYBR049C\nYLR336C\nYPL254W\nYPL039W\nYOL115W\nYLR014C\nYLR367W\nYDL117W\nYPR137W\nYDL227C\nYLR381W\nYKR010C\nYKL004W\nYPL012W\nYLR175W\nYOR243C\nYGL255W\nYJL098W\nYOR165W\nYMR006C\nYIL091C\nYBR106W\nYOR206W\nYGR090W\nYBR009C\nYMR093W\nYOL010W\nYFL045C\nYPL082C\nYPL094C\nYNR021W\nYHR072W\nYDR060W\nYCL014W\nYJR032W\nYDR303C\nYLR384C\nYCL054W\nYPL221W\nYLR459W\nYDL084W\nYJL056C\nYKR082W\nYHR103W\nYBR155W\nYJL076W\nYJL208C\nYDL074C\nYKL182W\nYNL102W\nYNL067W\nYPL211W\nYAR008W\nYMR194W\nYAL025C\nYNL313C\nYAR018C\nYBR060C\nYNL323W\nYLR355C\nYPL146C\nYOR310C\nYJR132W\nYNL061W\nYGR286C\nYML027W\nYDL208W\nYGR096W\nYBR267W\nYOR342C\nYPL122C\nYPL227C\nYGR216C\nYDR336W\nYOL121C\nYKR079C\nYNL065W\nYDR528W\nYOL080C\nYJR140C\nYIL009W\nYPR119W\nYMR230W\nYDR420W\nYFL025C\nYER073W\nYLR222C\nYOR372C\nYDR346C\nYOR315W\nYMR125W\nYOR247W\nYDR170C\nYNL216W\nYPL093W\nYNR067C\nYGR085C\nYBL081W\nYPL279C\nYOL088C\nYNL256W\nYLR187W\nYMR019W\nYER032W\nYLR357W\nYKL191W\nYDL042C\nYDR451C\nYPL241C\nYIL090W\nYCR084C\nYOR210W\nYOR099W\nYLR272C\nYML018C\nYGL022W\nYJR124C\nYJL186W\nYGL021W\nYBR088C\nYNL289W\nYDR045C\nYOR129C\nYEL032W\nYPR019W\nYMR003W\nYMR241W\nYNL206C\nYKR081C\nYFR028C\nYBR085W\nYPL207W\nYJR015W\nYEL076C\nYNL010W\nYDL031W\nYKL014C\nYOR108W\nYMR247C\nYJL207C\nYBR015C\nYHR099W\nYDR412W\nYAL059W\nYIL131C\nYOR304C-A\nYDR321W\nYKR099W\nYOL007C\nYLR088W\nYER013W\nYDR076W\nYNR017W\nYLR087C\nYDR418W\nYOR224C\nYCR072C\nYHL029C\nYPL217C\nYGL162W\nYNL090W\nYOR335C\nYPL255W\nYHR020W\nYPR138C\nYPL256C\nYDR213W\nYEL042W\nYMR199W\nYOR294W\nYBR296C\nYOR373W\nYLL014W\nYLR441C\nYBR129C\nYDR091C\nYMR001C\nYKR092C\nYIL128W\nYGR079W\nYPL244C\nYBL020W\nYLR373C\nYMR131C\nYJL200C\nYEL055C\nYPL126W\nYNL053W\nYML064C\nYCL037C\nYBR163W\nYML043C\nYOL124C\nYDR062W\nYNL219C\nYNL151C\nYML059C\nYOL105C\nYLL035W\nYIL132C\nYMR259C\nYMR217W\nYNL080C\nYJR063W\nYNL186W\nYOR196C\nYML119W\nYOR346W\nYLR448W\nYHR036W\nYOR340C\nYOR293W\nYDR017C\nYNL024C\nYBR135W\nYGR060W\nYHR144C\nYGR092W\nYLR405W\nYOR241W\nYJL193W\nYLR353W\nYNR009W\nYDR370C\nYFL034C-A\nYLR363W-A\nYNL291C\nYNR003C\nYBL079W\nYKL057C\nYDR179W-A\nYJL183W\nYIL140W\nYOL092W\nYCR043C\nYDR232W\nYJL122W\nYHR143W-A\nYLR084C\nYLL011W\nYGL014W\nYGL050W\nYMR127C\nYBR094W\nYOR175C\nYML113W\nYGR108W\nYNL299W\nYER118C\nYIL015W\nYJR097W\nYJR047C\nYOR229W\nYJL133W\nYDR518W\nYLL021W\nYBR162C\nYIL115C\nYBR133C\nYIL110W\nYBR061C\nYNL244C\nYLR237W\nYNL111C\nYLR347C\nYML081W\nYDR180W\nYAL022C\nYBR083W\nYBL023C\nYJR092W\nYMR300C\nYGL016W\nYOR359W\nYDL211C\nYCR092C\nYOR324C\nYKR024C\nYHR007C\nYLR004C\nYPL024W\nYPR190C\nYBL018C\nYML080W\nYJL051W\nYBR202W\nYJR031C\nYPL160W\nYGL201C\nYIL079C\nYPR187W\nYNL182C\nYHR149C\nYHR151C\nYNL298W\nYLR300W\nYDR507C\nYHR031C\nYGL092W\nYDR399W\nYCL063W\nYBL042C\nYHR167W\nYPR022C\nYHR061C\nYBR074W\nYGR217W\nYLR073C\nYPL141C");}
	else{
		return 0;
	}
};
