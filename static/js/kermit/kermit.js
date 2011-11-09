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
			alert('Error communicating with server');
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
					title : agent + '-' + action + ' execution...',
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
			alert('Error communicating with server');
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
			alert('Error communicating with server');
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
				title : operation + ' execution...',
				minHeight : 200,
				minWidth : 500
			});
			$("#" + deploy_form_name).show();

		}
	});
}

function getSqlDeployForm(base_url, deploy_form_name, operation, filters) {
	url = base_url + '/sqldeploy/get_deploy_form/' + deploy_form_name + '/' + operation + '/' + filters + '/';
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
			alert('Error communicating with server');
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
				title : operation + ' execution...',
				minHeight : 200,
				minWidth : 500
			});
			$("#" + deploy_form_name).show();

		}
	});
}

function sendRequestToMcollective(url, destination) {
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
	sendRequestToMcollective(url, destination)
}

function callMcollectiveWithTemplateRsp(url, destination) {
	sendRequestToMcollective(url, destination)
}