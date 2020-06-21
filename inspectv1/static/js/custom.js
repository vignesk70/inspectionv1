var online = false;
$(document).ready(function(){
if (navigator.onLine == true) {
	online = true;
	jQuery("document").ready(function(){
		 var values = [],
        keys = Object.keys(localStorage),
        i = keys.length;
		 while ( i-- ) {

			 if(keys[i].indexOf("savedvalues") !== -1)
			 { 
				 //alert(keys[i]); 
				 var dataval = localStorage.getItem(keys[i]);
				 console.log(dataval);
				 
				 dataval = JSON.parse(dataval);
				var form_data = new FormData();
				form_data.append("category_id", dataval.category_id);
				form_data.append("item_id", dataval.item_id);
				form_data.append("site_id", dataval.site_id);
				form_data.append("item_value", dataval.item_value);
				form_data.append("master_id", dataval.master_id);
				//form_data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
				form_data.append("item_image", dataval.file);
				 
				 
				 $.ajax({
					  url: "/add/",
					  type: "post",
					  data: form_data,
					  contentType: false,
					  processData: false,
					  async: false,
					  success: function (data) {
						  localStorage.removeItem(keys[i]);
					  },
            });
				 
			 }
			 
		 }
	
	});
	 
}
else{
	online =false;
}

})


function myfunction(id) {
  var type = $("#field_" + id)[0].type;

  if (type == "checkbox") {
    if ($("#field_" + id).is(":checked")) {
      $("#image_" + id).show();
    } else {
      $("#image_" + id).hide();
    }
  }
}

$(document).ready(function () {
  if ($("#siteid").length) {
    $("#siteid").autocomplete({
        minLength: 0,
        source: function (request, responce) {
          var form_data = new FormData();
          form_data.append("siteid", request.term);
		  key = request.term+"_searchsitesbyid";
		  var dataval = localStorage.getItem(key);	
		  if(online){
		  	dataval = null;
		  }
		  else{
		  		if(dataval == null){
					//alert("You haven't sync the online data, Please try when back online");
					return false;
				}
		  }
		 // alert(dataval);
			
		  if(dataval == null){	
          	$.ajax({
            url: "/getsites/",
            type: "post",
            data: form_data,
            contentType: false,
            processData: false,
            success: function (data) {
			  localStorage.setItem(key, data);	
              var obj = JSON.parse(data);

              if (obj.length != 0) {
                var output = [];
                for (index = 0; index < obj.length; index++) {
                  var newstring = {
                    label: obj[index][0],
                    value: obj[index][1],
                    desc: obj[index][2],
                  };

                  output[output.length] = newstring;
                }

                responce(output);
              } else {
                var result = [
                  {
                    label: 0,
                    value: 0,
                    desc: "No matches found",
                  },
                ];
                responce(result);
              }
            },
          });
		  }	
		  else{
		  	
			  data = dataval;  
			  var obj = JSON.parse(data);

              if (obj.length != 0) {
                var output = [];
                for (index = 0; index < obj.length; index++) {
                  var newstring = {
                    label: obj[index][0],
                    value: obj[index][1],
                    desc: obj[index][2],
                  };

                  output[output.length] = newstring;
                }

                console.log(output);
                responce(output);
              } else {
                var result = [
                  {
                    label: 0,
                    value: 0,
                    desc: "No matches found",
                  },
                ];
                responce(result);
			  
			  
			  
		  }
		  }
			  
        },
        focus: function (event, ui) {
          //$( "#siteid" ).val( ui.item.label );
          return false;
        },
        select: function (event, ui) {
          if (ui.item.value == 0) {
            return false;
          }
          $("#siteid").val(ui.item.label);
          $("#sitename").val(ui.item.value);

          return false;
        },
      })
      .autocomplete("instance")._renderItem = function (ul, item) {
      return $("<li>")
        .append("<div>" + item.desc + "</div>")
        .appendTo(ul);
    };

    $("#sitename")
      .autocomplete({
        minLength: 0,
        source: function (request, responce) {
          var form_data = new FormData();
          form_data.append("sitename", request.term);
			
		  key = request.term+"_searchsitesbyid";
		  var dataval = localStorage.getItem(key);	
		  if(dataval == null){		
			
          $.ajax({
            url: "/getsites/",
            type: "post",
            data: form_data,
            contentType: false,
            processData: false,
            success: function (data) {
			  localStorage.setItem(key, data);		
              var obj = JSON.parse(data);
              if (obj.length != 0) {
                var output = [];
                for (index = 0; index < obj.length; index++) {
                  var newstring = {
                    label: obj[index][0],
                    value: obj[index][1],
                    desc: obj[index][2],
                  };

                  output[output.length] = newstring;
                }

                console.log(output);
                responce(output);
              } else {
                var result = [
                  {
                    label: 0,
                    value: 0,
                    desc: "No matches found",
                  },
                ];
                responce(result);
              }
            },
          });
		  }else{
		   var data = dataval;
		  	var obj = JSON.parse(data);
              if (obj.length != 0) {
                var output = [];
                for (index = 0; index < obj.length; index++) {
                  var newstring = {
                    label: obj[index][0],
                    value: obj[index][1],
                    desc: obj[index][2],
                  };

                  output[output.length] = newstring;
                }

                console.log(output);
                responce(output);
              } else {
                var result = [
                  {
                    label: 0,
                    value: 0,
                    desc: "No matches found",
                  },
                ];
                responce(result);
              }
			  
		  }	  
			  
			  
        },
        focus: function (event, ui) {
          //$( "#siteid" ).val( ui.item.label );
          return false;
        },
        select: function (event, ui) {
          if (ui.item.value == 0) {
            return false;
          }
          $("#siteid").val(ui.item.label);
          $("#sitename").val(ui.item.value);

          return false;
        },
      })
      .autocomplete("instance")._renderItem = function (ul, item) {
      return $("<li>")
        .append("<div>" + item.desc + "</div>")
        .appendTo(ul);
    };
  }
});

$("document").ready(function () {
  $(document).on("click", ".submitbutton", function (event) {
   
    event.preventDefault();
    console.log("clicked");
    var throw_error;
    var category_id = $(this).attr("data-id");
    console.log(category_id);
	  if (navigator.onLine == true) {	  
			  console.log("still online");
	  }
    
    $("#category_" + category_id)
      .find("input[type=hidden]")
      .each(function () {
        if ($(this).prop("name") == "item_id") {
          var itemid = $(this).val();

          var itemvalue = $("#field_" + itemid).val();
          var itemimage = $("#image_" + itemid).val();
          var site_id = $("#site_id").val();
          var master_id = $("#master_id").val();
          if (master_id == 0) {
            master_id = "";
          }
          if ($("#throw_error_" + itemid).val() == "True") {
            throw_error = true;
            //alert($("#throw_error_" + itemid).val() + itemid);
          }
          if ($("#field_" + itemid).prop("type") == "checkbox") {
            itemvalue = $("#field_" + itemid).prop("checked");
            if ($("#field_" + itemid).prop("checked")) {
              if ($("#throw_error_" + itemid).val() == "True") {
                throw_error = true;
                //alert($("#throw_error_" + itemid).val() + itemid);
              }
            }
          }

          if (itemvalue != "") {
            var file = $("#image_" + itemid)[0].files[0];
            var form_data = new FormData();
            form_data.append("category_id", category_id);
            form_data.append("item_id", itemid);
            form_data.append("site_id", site_id);
            form_data.append("item_value", itemvalue);
            form_data.append("master_id", master_id);
            //form_data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
            form_data.append("item_image", file);
			  
			  var arr = new Object();
			 // arr.append("category_id", category_id);
			  arr["category_id"] = category_id;
			  arr["item_id"] = itemid;
			  arr["site_id"] = site_id;
			  arr["item_value"] = itemvalue;
			  arr["master_id"] = master_id;
			  arr["item_image"] = file;
			  
			  
			  
			 // console.log(arr);
			 // console.log("-----");

            //console.log(form_data);
            //console.log('{{ csrf_token }}'); return;
            
		     if (navigator.onLine == true) {	  
			  console.log("still online");
             	$.ajax({
              url: "/add/",
              type: "post",
              data: form_data,
              contentType: false,
              processData: false,
              async: false,
              success: function (data) {
                if (throw_error) {
                  /*if (
                    $("#field_" + itemid).prop("type") == "checkbox" &&
                    $("#field_" + itemid).is(":checked")
                  ) { */
                  $("#card_header_" + category_id + " .badge").addClass(
                    "badge-danger"
                  );
                  $("#card_header_" + category_id + " .badge").removeClass(
                    "badge-primary"
                  );

                  $("#card_header_" + category_id + " .fa").addClass(
                    "fa-exclamation-triangle"
                  );
                  $("#card_header_" + category_id + " .fa").removeClass(
                    "fa-question"
                  );

                  /* } else {
                    $("#card_header_" + category_id + " .badge").addClass("badge-success");
					$("#card_header_" + category_id + " .badge").removeClass("badge-primary");
					  
					$("#card_header_" + category_id + " .fa").addClass("fa-check-square");
                    $("#card_header_" + category_id + " .fa").removeClass("fa-question");  
                  } */
                } else {
                  $("#card_header_" + category_id + " .badge").addClass(
                    "badge-success"
                  );
                  $("#card_header_" + category_id + " .badge").removeClass(
                    "badge-primary"
                  );

                  $("#card_header_" + category_id + " .fa").addClass(
                    "fa-check-square"
                  );
                  $("#card_header_" + category_id + " .fa").removeClass(
                    "fa-question"
                  );
                }

                $("#savebutton_" + category_id).hide();
                jQuery("#master_id").val(data);
                $(".alert").show();
              },
            });
				 
			 }
			 else{
			     key = site_id+'--'+category_id+'--'+itemid+'_savedvalues';
				 var dataval = localStorage.setItem(key);
				 if(dataval == null){
				 	localStorage.setItem(key, JSON.stringify(arr));
				 }
			 }
				 
          }
        }
      });
  });
});

function updatedata() {

  
	
  var siteid = $("#siteid").val();
  var sitename = $("#sitename").val();
  var form_data = new FormData();
  form_data.append("sitename", sitename);
  form_data.append("siteid", siteid);
  //form_data.append("csrfmiddlewaretoken", csrftoken);
	
	var data = localStorage.getItem(siteid+"_data");
	
	if(online){
		data = null;
	}
	
	if(data == null){
		$.ajax({
		url: "/getcategories/",
		type: "post",
		data: form_data,
		contentType: false,
		processData: false,
		success: function (data) {
		  if (data == 0) {
			$(".createSite").hide();
			$("#choosesite").html("Entered Site Id doesn't Exist.");
			$("#choosesite").addClass("error");
			$("#choosesite").show();
		  } else {
			  localStorage.setItem(siteid+"_data", data);
			$(".createsiteclass").html(data);
		  }
		},
	  });
  }
  	else{
  		$(".createsiteclass").html(data);
  	}
	
}

function ajaxsubmit() {
  return false;
}

function showcard(id) {
  if ($("#category_" + id).hasClass("visible")) {
    $("#category_" + id).removeClass("visible");
    $("#category_" + id).addClass("invisible");
  } else {
    $("#category_" + id).removeClass("invisible");
    $("#category_" + id).addClass("visible");
  }
}

function geolocate() {
  alert("GET LOCATION");
  var x = document.getElementById("demo");

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }

  function showPosition(position) {
    x.innerHTML =
      "Latitude: " +
      position.coords.latitude +
      "<br>Longitude: " +
      position.coords.longitude;
  }
}

function loaddata(){

var siteid = $("#siteid").val();
	
window.location.href="/inspection/?type=site&site=101004";	
	
}
//test

