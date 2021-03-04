var online = false;

navigator.serviceWorker.ready.then(function (registration) {
  console.log('Service Worker Ready')
  return registration.sync.register('sendFormData')
}).then(function () {
  console.log('sync event registered')
}).catch(function () {
  // system was unable to register for a sync,
  // this could be an OS-level restriction
  console.log('sync registration failed')
});


$(document).ready(function () {
  if (navigator.onLine == true) {
    online = true;

    readItemfromDB();
    // jQuery("document").ready(function () {
    //   var values = [],
    //     keys = Object.keys(localStorage),
    //     i = keys.length;

    //   while (i--) {

    //     if (keys[i].indexOf("savedvalues") !== -1) {
    //       //alert(keys[i]);
    //       var dataval = localStorage.getItem(keys[i]);
    //       console.log(dataval);

    //       dataval = JSON.parse(dataval);
    //       var form_data = new FormData();
    //       form_data.append("category_id", dataval.category_id);
    //       form_data.append("item_id", dataval.item_id);
    //       form_data.append("site_id", dataval.site_id);
    //       form_data.append("item_value", dataval.item_value);
    //       form_data.append("master_id", dataval.master_id);
    //       //form_data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
    //       if (dataval.item_image) {
    //         form_data.append("item_image", converBase64toBlob(dataval.item_image, dataval.item_type), dataval.item_image_name);
    //       }
    //       form_data.append("dataadd", dataval.dateadd)

    //       readItemfromDB();

    //       $.ajax({
    //         url: "/add/",
    //         type: "post",
    //         data: form_data,
    //         contentType: false,
    //         processData: false,
    //         async: false,
    //         success: function (data) {
    //           localStorage.removeItem(keys[i]);
    //           if (localStorage.getItem(keys[i].split("--", 1)[0].concat("_data"))) {
    //             localStorage.removeItem(keys[i].split("--", 1)[0].concat("_data"))
    //           }

    //         },
    //       });

    //     }

    //   }

    // });

  } else {
    online = false;
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
          key = request.term + "_searchsitesbyid";
          var dataval = localStorage.getItem(key);
          if (online) {
            dataval = null;
          } else {
            if (dataval == null) {
              //alert("You haven't sync the online data, Please try when back online");
              return false;
            }
          }
          // alert(dataval);

          if (dataval == null) {
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
                  var result = [{
                    label: 0,
                    value: 0,
                    desc: "No matches found",
                  }, ];
                  responce(result);
                }
              },
            });
          } else {

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
              var result = [{
                label: 0,
                value: 0,
                desc: "No matches found",
              }, ];
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

          key = request.term + "_searchsitesbyid";
          var dataval = localStorage.getItem(key);
          if (dataval == null) {

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
                  var result = [{
                    label: 0,
                    value: 0,
                    desc: "No matches found",
                  }, ];
                  responce(result);
                }
              },
            });
          } else {
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
              var result = [{
                label: 0,
                value: 0,
                desc: "No matches found",
              }, ];
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
    $(".upload").show();
    $(".alert-success").hide();
    deleteonsave = true;
    event.preventDefault();
    console.log("clicked");
    var throw_error;
    var category_id = $(this).attr("data-id");
    console.log(category_id);
    if (navigator.onLine == true) {
      console.log("still online");
    }

    // Give the UI time to render because ajax.async:false freezes the UI on chrome
    setTimeout(function() {
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
          event = new Date().toISOString()
          if (itemvalue != "") {
            var file = $("#image_" + itemid)[0].files[0];
            var form_data = new FormData();
            form_data.append("category_id", category_id);
            form_data.append("item_id", itemid);
            form_data.append("site_id", site_id);
            form_data.append("item_value", itemvalue);
            form_data.append("master_id", master_id);
            form_data.append("deleteonsave",deleteonsave);
            deleteonsave=false;
            //form_data.append("csrfmiddlewaretoken", '{{ csrf_token }}');


            form_data.append("dateadd", event.split('T')[0]);


            var arr = new Object();
            // arr.append("category_id", category_id);
            arr["category_id"] = category_id;
            arr["item_id"] = itemid;
            arr["site_id"] = site_id;
            arr["item_value"] = itemvalue;
            arr["master_id"] = master_id;
            if (file) arr["item_image"] = file;
            arr["dateadd"] = event.split('T')[0];


            key = site_id + '--' + category_id + '--' + itemid + '_savedvalues';
            if (file) {
              form_data.append("item_image", file, file.name);
              //processFile(key, file, arr, form_data);
            }
            console.log('arr', arr);
            console.log("form data", form_data)
            var msg = {
              'form_data': form_data
            }

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
                /*xhr: function () {
                  var xhr = $.ajaxSettings.xhr();
                  xhr.upload.onprogress = function (e) {
                    console.log("in xhr function");
                    // For uploads
                    if (e.lengthComputable) {
                      console.log(e.loaded / e.total);
                    }
                  };
                  return xhr;
                },*/
                success: function (data) {
                  if (throw_error) {
                    /*if (
                      $("#field_" + itemid).prop("type") == "checkbox" &&
                      $("#field_" + itemid).is(":checked")
                    ) { */
                    $("#card_header_" + category_id + " .badge").removeClass("badge-warning");

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
                    $("#card_header_" + category_id + " .badge").removeClass("badge-warning")

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

                  //$("#savebutton_" + category_id).hide();
                  // $(showcard(category_id));
                  jQuery("#master_id").val(data);
                  $(".alert-success").show();
                },
              });

            } else {
              //key = site_id + '--' + category_id + '--' + itemid + '_savedvalues';
              //$(showcard(category_id));
              $("#card_header_" + category_id + " .badge").addClass(
                "badge-warning");
              //saveToLocalStorage(key, arr);
              addToDb(key, arr, file);
              //readItemfromDB();
              // var dataval = localStorage.getItem(key);
              // if (dataval == null) {
              //   localStorage.setItem(key, JSON.stringify(arr));
              // } else { localStorage.setItem(key, JSON.stringify(arr)); }
            }

          }
        }
      });
      console.log("at the end");
      $(".upload").fadeOut("fast");
    }, 30);
    $(showcard(category_id));
  });
});

function updatedata() {



  var siteid = $("#siteid").val();
  var sitename = $("#sitename").val();
  var form_data = new FormData();
  form_data.append("sitename", sitename);
  form_data.append("siteid", siteid);
  //form_data.append("csrfmiddlewaretoken", csrftoken);

  var data = localStorage.getItem(siteid + "_data");

  if (online) {
    data = null;
  }

  if (data == null) {
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
          localStorage.setItem(siteid + "_data", data);
          $(".createsiteclass").html(data);
        }
      },
    });
  } else {
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
  //alert("GET LOCATION");
  var x = document.getElementById("demo");

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }

  function showPosition(position) {
    // x.innerHTML =
    //   "Latitude: " +
    //   position.coords.latitude +
    //   "<br>Longitude: " +
    //   position.coords.longitude;
    var slat = position.coords.latitude;
    var slon = position.coords.longitude;
    var form_data = new FormData();
    form_data.append("slat", slat);
    form_data.append("slon", slon);
    $.ajax({
      url: "/getnearestsite/",
      type: "post",
      data: form_data,
      contentType: false,
      processData: false,
      success: function (data) {
        var obj = JSON.parse(data)
        //alert(obj)
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
          //alert(obj);
          //jQuery('#locate').append('<select id="' + output.label + '"></select>');
          var create = '<select id="test" class="form-control"> <option>-Select one- </option>';
          for (var i = 0; i < output.length; i++) {
            create += '<option name="' + output[i].value + '" value="' + output[i].label + '">' + output[i].desc + '</option>';

          }
          create += '</select>'
          $('#locate').append(create)
          $('#test').change(function () {
            var val = $(this).find('option:selected').val();
            var siten = $(this).find('option:selected[name]').text().split('-')
            //alert(siten[1])
            //alert('i selected: ' + val);
            $('#siteid').val(val);
            $('#sitename').val(siten[1]);
            $('#test').remove();

          });
        };
      }
    });




  }
}

function loaddata() {

  var siteid = $("#siteid").val();

  window.location.href = "/inspection/?type=site&site=101004";

}
//test
$(document).on("click", ".submitbutton2", function (event) {
  event.preventDefault();
  for (i = 0; i < document.getElementsByClassName("submitbutton").length; i++) {
    document.getElementsByClassName("submitbutton")[i].click();
  }
});

function processFile(siteKey, file, arr, form_data) {
  if (!file) {
    return;
  }
  arr["item_image_name"] = file.name;
  form_data.append("item_image_" + file.name, file);
  form_data.append("item_type", file.type);
  //convertFileToBase64(siteKey, file, arr, file.type);
}

function convertFileToBase64(siteKey, file, arr, filetype) {
  // encode the file using the FileReader API
  const reader = new FileReader();

  //implement what happens after file is read.
  reader.onloadend = () => {

    // use a regex to remove data url part
    const arrObj = arr;
    const base64String = reader.result
      .replace('data:', '')
      .replace(/^.+,/, '');

    // log to console
    //console.log(base64String) // logs wL2dvYWwgbW9yZ...

    //now save to array and save to local storage
    arrObj["item_image"] = base64String;
    arrObj["item_type"] = filetype;
    //arrObj["file"] = file;
    saveToLocalStorage(siteKey, arrObj);
    //addToDb(siteKey, arrObj, file);
    //readItemfromDB();

    //TODO: this is just a test. this line should be moved to when loading the data from localstorage.absent
    //convertBase64ToFile(key,base64String, file.name);

  };
  //start reading the file.
  reader.readAsDataURL(file);
}

function convertBase64ToFile(key, b64, fileName) {
  var f;
  var blob = converBase64toBlob(b64, "application/png");
  //TODO: this is not working. need to learn how to convert blob to File, or if it can be used as a Blob, since File 'inherits' Blob
  f = new File(blob, fileName);
}

function converBase64toBlob(content, contentType) {
  contentType = contentType || '';
  var sliceSize = 512;
  var byteCharacters = window.atob(content); //method which converts base64 to binary
  var byteArrays = [];
  for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    var slice = byteCharacters.slice(offset, offset + sliceSize);
    var byteNumbers = new Array(slice.length);
    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }
    var byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);
  }
  var blob = new Blob(byteArrays, {
    type: contentType
  }); //statement which creates the blob
  return blob;
}

function saveToLocalStorage(key, arr) {
  var dataval = localStorage.getItem(key);
  if (dataval == null) {
    localStorage.setItem(key, JSON.stringify(arr));
  } else {
    localStorage.setItem(key, JSON.stringify(arr));
  }
}

const DB_NAME = 'images_db';
const DB_VERSION = 1; // Use a long long for this value (don't use a float
const DB_STORE_NAME = 'site_images';

var db;
var current_key;

//initialize the database
function opendb() {
  console.log("open db");

  var req = indexedDB.open(DB_NAME, DB_VERSION);
  req.onsuccess = function (evt) {
    db = this.result;
    console.log("Open db done")
  };
  req.onerror = function (evt) {
    console.log("Open DB: ", evt.target.errorCode)
  };

  req.onupgradeneeded = function (evt) {
    console.log("openDb upgrade needed");
    var store = evt.currentTarget.result.createObjectStore(
      DB_STORE_NAME, {
        keyPath: 'sitekey'
      });
  };
}

//get the objectstore for transaction
function getObjectStore(store_name, mode) {
  var tx = db.transaction(store_name, mode);
  return tx.objectStore(store_name);
};

//add the array to the db
function addToDb(key, arr, file) {

  console.log("addfile arguments:", arguments);
  obj = {
    sitekey: key,
    payload: arr,
    blob: file
  };
  var store = getObjectStore(DB_STORE_NAME, "readwrite");
  var req;
  try {
    req = store.put(obj)
  } catch (error) {
    if (error.name == "DataCloneError")
      console.log("error with this browser");
    throw error;
  }
  req.onsuccess = function (e) {
    key = e.target.result;
    current_key = key
    console.log("adding file", key)
    //displayFile(current_key, store)
  }
  req.onerror = function () {
    console.log("err with file")
  }
};

function readItemfromDB() {
  var savedRequests = [];
  var total = 0;
  var count = 0;
  var req = indexedDB.open(DB_NAME, DB_VERSION);
  req.onsuccess = function (evt) {
    db = this.result;
    console.log("Open db done")
    var store = getObjectStore(DB_STORE_NAME, "readwrite");
    var req;
    try {
      req = store.count();
      req.onsuccess = function (e) {
        console.log('Count: ', e.target.result);
        total = e.target.result;
      }
    } catch (error) {
      console.log(error.errorCode);
      throw error
    }

    req = getObjectStore(DB_STORE_NAME).openCursor();
    req.onsuccess = function (e) {
      var cursor = e.target.result;
      if (cursor != null) $(".alert-danger").show();

      if (cursor) {
        //console.log("cursor:", cursor.value)
        savedRequests.push(cursor.value);
        cursor.continue()
      } else {
        for (let savedRequest of savedRequests) {
          console.log('saved request', savedRequest);
          var requestUrl = '/add/';
          var method = 'POST';
          keys = savedRequest.payload.keys;
          console.log(savedRequest.payload.item_id)
          var dataval = savedRequest.payload
          console.log(dataval);

          //dataval = JSON.parse(dataval);
          var form_data = new FormData();
          form_data.append("category_id", dataval.category_id);
          form_data.append("item_id", dataval.item_id);
          form_data.append("site_id", dataval.site_id);
          form_data.append("item_value", dataval.item_value);
          form_data.append("master_id", dataval.master_id);
          //form_data.append("csrfmiddlewaretoken", '{{ csrf_token }}');
          if (dataval.item_image) {
            form_data.append("item_image", dataval.item_image, dataval.item_image.name);
          }
          form_data.append("dateadd", dataval.dateadd)
          var payload = JSON.stringify(savedRequest.payload);
          var file = savedRequest.file
          var headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
          fetch(requestUrl, {
            //headers: headers,
            method: method,
            body: form_data
          }).then(function (response) {
            console.log('server response:', response);
            if (response.status < 400) {
              getObjectStore(DB_STORE_NAME, 'readwrite').delete(savedRequest.sitekey)
            }
          }).catch(function (error) {
            console.log('Send to Server failed:', error);
            throw error
          }).finally(function() {
            ++count;
            //console.log('background upload completed', count, total);
            if (count === total) $(".alert-danger").hide();
          })
        }
      }
    }
  };
  
};

function getissuedetails(id) {
  alert('called function with value' + id)
  var form_data = new FormData();
  form_data.append("id", id);
  $.ajax({
    url: "/displayissuedetail/",
    type: "post",
    data: form_data,
    contentType: false,
    processData: false,
    success: function (data) {
      var obj = JSON.parse(data)
      alert(obj)
    }
  });

};

function validatefile(imageid) {
  //console.log(imageid);
  const fi = document.getElementById(imageid);
  // Check if any file is selected.
  if (fi.files.length > 0) {
    for (var i = 0; i < fi.files.length; i++) {
      var fsize = fi.files.item(i).size;
      var file = Math.round((fsize / 1024));
      // The file size limit.
      if (file > 12288) {
          alert("File size too large - Attachment must be less than 12MB.");
          fi.value = null;
      }
    }
  }

};
opendb()