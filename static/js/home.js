

$(document).ready(function() {


$.ajaxSetup({
	data: {
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
});
$("#submit").on('click',function() {
	var id=$('#chr').val()+'_'+$('#ipos').val()+'-'+$('#epos').val()
	$.ajax({
		url: "/t50504/ajax_calcu/",
		data: {
			'keyname':$('#submit').attr('name'),
			'chrname':$('#chr').val(),
			'ipos':$('#ipos').val(),
			'epos':$('#epos').val(),
			
		},
		success: function(data) {
			console.log('ajax success')
			
			if(String(data['status'])=='finish'){
				$('#result').append("<p>Analysis: "+data['status']+",Download:<button class="+id+" onclick=\"window.location.href='/t50504/download/?file="+id+"'\">Info_"+id+'</p>');
			}
			else{
				$('#result').append('Analysis: '+String(data['status']));
			}
			//返回值 data 在這裡是一個列表
			for (var i in data) {
				// 把 data 的每一項顯示在網頁上
                                console.log(data)
                                console.log(data[i])				
			}

		},
		type: "POST",
		dataType: "json"
	});


});

$("#ask_sum").on('click',function() {
	var sumbtn = $('#ask_sum').attr('name')
	$.ajax({
		url: "/t50504/ajax_sum/",
		data: {
			'sum_com':$('#ask_sum').attr('name'),
		},
		success: function(data) {
			console.log('ajax summary success')
			$('#result').append("<p>Download:<button class="+sumbtn+" onclick=\"window.location.href='/t50504/download/?file=summary'\">Info_summary</p>")
			//返回值 data 在這裡是一個列表
			for (var i in data) {
				// 把 data 的每一項顯示在網頁上
				
			}

			},
		type: "POST",
		dataType: "json"
	});


});

   
    
});
