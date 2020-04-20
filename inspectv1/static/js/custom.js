function myfunction(id){
	  var type = $("#field_"+id)[0].type;
	  
	  if(type == "checkbox"){
	  	if ($("#field_"+id).is(":checked")) { 
             $("#image_"+id).show(); 
         }
		 else{
		 	$("#image_"+id).hide();
		 }
	  }
	}



 $(document).ready(function () {  
	 
	             var projects = [
				  {
					value: "jquery",
					label: "jQuery",
					desc: "the write less, do more, JavaScript library",
					icon: "jquery_32x32.png"
				  },
				  {
					value: "jquery-ui",
					label: "jQuery UI",
					desc: "the official user interface library for jQuery",
					icon: "jqueryui_32x32.png"
				  },
				  {
					value: "sizzlejs",
					label: "Sizzle JS",
					desc: "a pure-JavaScript CSS selector engine",
					icon: "sizzlejs_32x32.png"
				  }
				];
				
	 
	                $( "#siteid" ).autocomplete({
					  minLength: 0,
					  source: function (request, responce) { 
						  
						  var form_data = new FormData();	
						  form_data.append("siteid", request.term);	
						  
						  $.ajax({
							url:  '/inspect/getsites/',
							type:  'post',
							data : form_data,
							contentType: false,
							processData: false,
							success:  function (data) {
						    
							
							var obj = JSON.parse(data);
							
							if(obj.length != 0){
							var output = [];
							for (index = 0; index < obj.length; index++) {
							
								
								var newstring = {
									  label : obj[index][0],
									  value  : obj[index][1],
									  desc     :  obj[index][2],
									};

								
								output[output.length] = newstring;
							}	

							console.log(output);	
							responce(output)
							}
							else{
								var result = [
								{
									label: 0, 
									value: 0,
									desc: 'No matches found', 
								},
								];
							responce(result);
							}


							}
						})  
					   },	  
					  focus: function( event, ui ) {
						//$( "#siteid" ).val( ui.item.label );
						return false;
					  },
					  select: function( event, ui ) {
						if(ui.item.value == 0){
						 return false;
						}
						$( "#siteid" ).val( ui.item.label );
						$( "#sitename" ).val( ui.item.value );
						
						return false;
					  }
					})
					.autocomplete( "instance" )._renderItem = function( ul, item ) {
						
					  return $( "<li>" )
						.append( "<div>"  + item.desc + "</div>" )
						.appendTo( ul );
					};
				  
	 
	 				$( "#sitename" ).autocomplete({
					  minLength: 0,
					  source: function (request, responce) { 
						  
						  var form_data = new FormData();	
						  form_data.append("sitename", request.term);	
						  
						  $.ajax({
							url:  '/inspect/getsites/',
							type:  'post',
							data : form_data,
							contentType: false,
							processData: false,
							success:  function (data) {
						    
							
							var obj = JSON.parse(data);
							if(obj.length != 0){
							var output = [];
							for (index = 0; index < obj.length; index++) {
							
								
								var newstring = {
									  label : obj[index][0],
									  value  : obj[index][1],
									  desc     :  obj[index][2],
									};

								
								output[output.length] = newstring;
							}	

							console.log(output);	
							responce(output);
							}
							else{
								var result = [
								{
									label: 0, 
									value: 0,
									desc: 'No matches found', 
								},
								];
								responce(result);
							}


							}
						})  
					   },	  
					  focus: function( event, ui ) {
						//$( "#siteid" ).val( ui.item.label );
						return false;
					  },
					  select: function( event, ui ) {
						if(ui.item.value == 0){
						 return false;
						}
						$( "#siteid" ).val( ui.item.label );
						$( "#sitename" ).val( ui.item.value );
						
						return false;
					  }
					})
					.autocomplete( "instance" )._renderItem = function( ul, item ) {
					  return $( "<li>" )
						.append( "<div>"  + item.desc + "</div>" )
						.appendTo( ul );
					};
	 

	 
	 
             
        }); 


$("document").ready(function(){
		$(document).on('click','.submitbutton',function(event){
		//$(".submitbutton").live( "click",function(event){
		  event.preventDefault();
			
			var category_id = $(this).prop('id');
			
			$("#category_"+category_id).find("input[type=hidden]").each(function(){
				
				if( $(this).prop('name') == "item_id" ) {
				//alert($(this).html());
				var itemid =  $(this).val();
				
				var itemvalue = $("#field_"+itemid).val();
				var itemimage = $("#image_"+itemid).val();
				var site_id = $("#site_id").val();
				
				
				if($("#field_"+itemid).prop('type') == 'checkbox'){
					itemvalue = $("#field_"+itemid).prop('checked');
				
				}
				
				if(itemvalue != ''){

				var file = $("#image_"+itemid)[0].files[0];	
				var form_data = new FormData();	
				form_data.append("category_id", category_id);	
				form_data.append("item_id", itemid);	
				form_data.append("site_id", site_id);	
				form_data.append("item_value", itemvalue);	
				//form_data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
				form_data.append("item_image", file); 
					
				console.log(form_data); 	
				//console.log('{{ csrf_token }}'); return;	
				
				$.ajax({
					url:  '/inspect/add/',
					type:  'post',
					data : form_data,
          			contentType: false,
        			processData: false,
					success:  function (data) {
						if( $("#throw_error_"+itemid).val()  ){
							$( "#card_header_"+category_id ).addClass( "base_error" );
						}
							
					   $(".alert").show();	

           

					}
				});
				
			}	}
				
				
			});
			
		});
		
	})
	
	function updatedata(){
		var siteid = $("#siteid").val();
		var sitename = $("#sitename").val();
		var form_data = new FormData();	
		form_data.append("sitename", sitename);	
		form_data.append("siteid", siteid);	
		//form_data.append("csrfmiddlewaretoken", csrftoken);
		
		$.ajax({
					url:  '/inspect/getcategories/',
					type:  'post',
					data : form_data,
          			contentType: false,
        			processData: false,
					success:  function (data) {
						if(data == 0){
							$(".createSite").hide();
							$("#choosesite").html("Entered Site Id doesn't Exist.");
							$("#choosesite").addClass("error");
							$("#choosesite").show();
						}else{
							$(".createsiteclass").html(data);
						}	
					}
				});
		
		
	}
	
	function ajaxsubmit(){
		return false;
		
	}
	
	function showcard(id){
		if( $( "#category_"+id ).hasClass('visible') ){
			$( "#category_"+id ).removeClass('visible');
			$( "#category_"+id ).addClass('invisible');
		}else{
			$( "#category_"+id ).removeClass('invisible');
			$( "#category_"+id ).addClass('visible');
		}
	}
	