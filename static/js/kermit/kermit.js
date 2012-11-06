function contains(a, obj) {
    var i = a.length;
    while (i--) {
       if (a[i] === obj) {
           return true;
       }
    }
    return false;
}

function getExecutionForm(base_url, execution_dialog_name, agent, action, filters, response_container_name) {
	url = base_url + '/agent/action/get_dialog_form/' + agent + '/' + action + '/' + filters + '/' + execution_dialog_name + '/' + response_container_name + '/';
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "html",
		error : function() {
			//TODO: Show error message
			//$('#loading').hide();
			alert('Cannot get execution form. Error communicating with server');
		},
		beforeSend : function() {
			//$('#loading').show();
		},
		complete : function() {
			//$('#loading').hide();
		},
		success : function(data) {
			if(data != 'None') {
				$("#" + execution_dialog_name).html(data);
				$("#" + execution_dialog_name).dialog({
					modal : true,
					title : 'Agent/Action execution form',
					minHeight : 200,
					minWidth : 500
				});
				$("#" + execution_dialog_name).show();
			} else {
				callMcollective(base_url + '/restapi/mcollective/' + filters + '/' + agent + '/' + action + '/', response_container_name);
			}

		}
	});
}

function getUploadForm(url, upload_dialog) {
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "html",
		error : function() {
			//TODO: Show error message
			//$('#loading').hide();
			alert('Cannot get upload form. Error communicating with server');
		},
		beforeSend : function() {
			//$('#loading').show();
		},
		complete : function() {
			//$('#loading').hide();
		},
		success : function(data) {
			$("#" + upload_dialog).html(data);
			$("#" + upload_dialog).dialog({
				modal : true,
				title : 'Upload Dialog',
				minHeight : 200,
				minWidth : 500
			});
			$("#" + upload_dialog).show();

		}
	});
}

function getDeployForm(base_url, platform_name, deploy_form_name, operation, filters) {
	url = base_url + '/platform/' + platform_name + '/get_deploy_form/' + deploy_form_name + '/' + operation + '/' + filters + '/';
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "html",
		error : function() {
			//TODO: Show error message
			//$('#loading').hide();
			alert('Cannot get deploy form. Error communicating with server');
		},
		beforeSend : function() {
			//$('#loading').show();
		},
		complete : function() {
			//$('#loading').hide();
		},
		success : function(data) {
			$("#" + deploy_form_name).html(data);
			$("#" + deploy_form_name).dialog({
				modal : true,
				title : 'Operation execution form',
				minHeight : 200,
				minWidth : 500
			});
			$("#" + deploy_form_name).show();

		}
	});
}

function getForm(base_url, platform_name, form_name, operation, filters) {
	url = base_url + '/platform/' + platform_name + '/get_form/' + form_name + '/' + operation + '/' + filters + '/';
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "html",
		error : function() {
			//TODO: Show error message
			//$('#loading').hide();
			alert('Cannot get desired form. Error communicating with server');
		},
		beforeSend : function() {
			//$('#loading').show();
		},
		complete : function() {
			//$('#loading').hide();
		},
		success : function(data) {
			$("#" + form_name).html(data);
			$("#" + form_name).dialog({
				modal : true,
				title : 'Operation execution form',
				minHeight : 200,
				minWidth : 500
			});
			$("#" + form_name).show();

		}
	});
}


function getSqlExecutionForm(base_url, platform_name, deploy_form_name, operation, filters) {
	url = base_url + '/platform/' + platform_name + '/get_execute_form/' + deploy_form_name + '/' + operation + '/' + filters + '/';
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "html",
		error : function() {
			//TODO: Show error message
			//$('#loading').hide();
			alert('Cannot get sql form. Error communicating with server');
		},
		beforeSend : function() {
			//$('#loading').show();
		},
		complete : function() {
			//$('#loading').hide();
		},
		success : function(data) {
			$("#" + deploy_form_name).html(data);
			$("#" + deploy_form_name).dialog({
				modal : true,
				title : 'Operation execution form',
				minHeight : 200,
				minWidth : 500
			});
			$("#" + deploy_form_name).show();

		}
	});
}

function getLogForm(base_url, platform_name, container, operation, filters) {
	url = base_url + '/platform/' + platform_name + '/get_log_form/' + container + '/' + operation + '/' + filters + '/';
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "html",
		error : function() {
			//TODO: Show error message
			//$('#loading').hide();
			alert('Cannot get log form. Error communicating with server');
		},
		beforeSend : function() {
			//$('#loading').show();
		},
		complete : function() {
			//$('#loading').hide();
		},
		success : function(data) {
			$("#" + container).html(data);
			$("#" + container).dialog({
				modal : true,
				title : 'Operation execution form',
				minHeight : 200,
				minWidth : 500
			});
			$("#" + container).show();

		}
	});
}

function sendRequestToMcollectiveSync(url, destination) {
	$("#" + destination).empty();
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "json",
		error : function() {
			//TODO: Show error message
			$('#loading').hide();
		},
		beforeSend : function() {
			$('#loading').show();
		},
		complete : function() {
			$('#loading').hide();
		},
		timeout: 600000,
		success : function(data) {
			$("#" + destination).empty();
			if(data.type == 'json') {
				for(i in data.response) {
					resp = data.response[i];
					content = '<strong>' + resp.sender + '</strong>';
					content += '<ul>';
					content += '<li> Status Code: ' + resp.statuscode + '</li>';
					content += '<li> Status Message: ' + resp.statusmsg + '</li>';
					content += '<li> Data: ' + JSON.stringify(resp.data) + '</li>';
					content += '</ul>';
					$(content).appendTo("#response-container");
				}
			} else if(data.type == 'html') {
				$("#" + destination).html(data.response);
			}
		}
	});
}

function sendRequestToMcollectiveCallBack(url, callBackFunction) {
	$.ajax({
		// The link we are accessing.
		url : url,
		// The type of request.
		type : "get",
		// The type of data that is getting returned.
		dataType : "json",
		error : function() {
			//TODO: Show error message
			$('#loading').hide();
		},
		beforeSend : function() {
			$('#loading').show();
		},
		complete : function() {
			$('#loading').hide();
		},
		timeout: 600000,
		success : callBackFunction()
	});
}

function sendRequestToMcollective(url, destination) {
	$("#" + destination).empty();
	$('#modalprogress').dialog({
			modal : true,
			title : 'Progress...',
			height : 100,
			width : 500
		});
		$( "#progressbar" ).progressbar({ value: 0 });
		$( "#taskstate").html('<b>Waiting...	</b>');
		//$("#" + destination).empty();
		$.get(url, function(data) {
			//$('#' + destination).html(data);
			var checkStatus = function() {
		    	$.getJSON(data.update_url, function(result) {
		    		$( "#progressbar").progressbar({ value: result.value });
					$( "#taskstate").html('<b>' + result.state + '</b>');	
			        if(result.state!='SUCCESS' && result.state!='FAILURE' && result.state!=undefined) {
			            setTimeout(checkStatus, 2000);
			        } else {
			        	if(result.type == 'json') {
							for(i in result.response) {
								resp = result.response[i];
								content = '<strong>' + resp.sender + '</strong>';
								content += '<ul>';
								content += '<li> Status Code: ' + resp.statuscode + '</li>';
								content += '<li> Status Message: ' + resp.statusmsg + '</li>';
								content += '<li> Data: ' + JSON.stringify(resp.data) + '</li>';
								content += '</ul>';
								$(content).appendTo("#response-container");
							}
						} else if(result.type == 'html') {
							$("#" + destination).html(result.response);
						}
			        	$('#modalprogress').dialog('close');
			        }
		        // do something else
    		 	});
			}
			if (data.UUID) {
				checkStatus();
			} else {
				if (data.error) {
					$( "#taskstate").html(data.error);
				}
				//$('#modalprogress').dialog('close');	
			}
		});
}

function randomString() {
	var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
	var string_length = 8;
	var randomstring = '';
	for (var i=0; i<string_length; i++) {
		var rnum = Math.floor(Math.random() * chars.length);
		randomstring += chars.substring(rnum,rnum+1);
	}
	return randomstring;
}

function callMcollective(url, destination) {
	sendRequestToMcollective(url, destination);
}

function callMcollectiveModal(url, destination) {
	$('#'+destination).dialog({
            width: 600,
            modal: true,
    });
	sendRequestToMcollective(url, destination);
}

function callMcollectiveWithTemplateRsp(url, destination) {
	sendRequestToMcollective(url, destination)
}

function openVNC(vncproxy_url, redirect_url) {
	sendRequestToMcollectiveCallBack(vncproxy_url, function() { window.open(redirect_url, '_blank'); } );
}

jQuery.expr[':'].Contains = function(a,i,m){
  return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
};

function filterList(header, list) {
    var form = $("<form>").attr({"class":"filterform","action":"#"}),
        input = $("<input>").attr({"class":"filterinput","type":"text"});
    $(form).append("<span>Class Filter:</span> ").append(input).appendTo(header);
 
    $(input)
      .change( function () {
        var filter = $(this).val();
        if(filter) {
 
          $matches = $(list).find('li:Contains(' + filter + ')');
          $('li', list).not($matches).slideUp();
          $matches.slideDown();
 
        } else {
          $(list).find("li").slideDown();
        }
        return false;
      })
    .keyup( function () {
        $(this).change();
    });
}

function filterTree(searchTerm, dynatree) { 
    var startNode = $("#" + dynatree).dynatree("getRoot"); 
    startNode.visit(function(node) 
    {
        if (node.data.title) 
        { 
            // Filter currently visible non-root nodes. 
            if (node.data.title.toUpperCase().indexOf(searchTerm.toUpperCase()) >= 0) 
            { 
            	if (searchTerm.length == 0) {
            		if (node.isVisible() && node.getParent()!=null) {
            			node.getParent().expand(false);	
            		} 	
            	} else {
            		if (!node.isVisible() && node.getParent()!=null) {
            			node.getParent().expand(true);
            		}
            	}
                // Make sure we and all our parents are visible 
                node.visitParents(function(node) 
                { 
                    $(node.li).show(); 
                    return (node.parent != null); 
                }, true); 

                // Terminate the traversal of this branch since the  node matches 
                //return 'skip'; 
            } else { 
                $(node.li).hide(); 
            } 
        } 
    });
}

function showMessageDialog(message, confirm_button) {
        $('#message-dialog').text(message);
        var buttons = {};

        buttons[ confirm_button ] = function() {
            $("#message-dialog").dialog("close");
        };
        $('#message-dialog').dialog({
        autoOpen: false,
        width: 400,
        modal: true,
        resizable: false,
        buttons: buttons
    });
    $("#message-dialog").show();

    $('#message-dialog').dialog('open');
}

function editNode(node){
  var prevTitle = node.data.title,
    tree = node.tree;
  // Disable dynatree mouse- and key handling
  tree.$widget.unbind();
  // Replace node with <input>
  $(".dynatree-title", node.span).html("<input id='editNode' value='" + prevTitle + "'>");
  // Focus <input> and bind keyboard handler
  $("input#editNode")
    .focus()
    .keydown(function(event){
      switch( event.which ) {
      case 27: // [esc]
        // discard changes on [esc]
        $("input#editNode").val(prevTitle);
        $(this).blur();
        break;
      case 13: // [enter]
        // simulate blur to accept new value
        $(this).blur();
        break;
      }
    }).blur(function(event){
      // Accept new value, when user leaves <input>
      var title = $("input#editNode").val();
      node.setTitle(title);
      // Re-enable mouse and keyboard handlling
      tree.$widget.bind();
      node.focus();
    });
}
