
//customer
function hideCustomerFunction(){
	document.getElementById('intro_officer').style.display = 'none';
	document.getElementById('register_request_list').style.display = 'none';
	document.getElementById('sample_request_list').style.display = 'none';
	document.getElementById('hold_request_list').style.display = 'none';


}

function register_request_listFunction(){
	hideCustomerFunction();
	document.getElementById('register_request_list').style.display = 'block';

}


function sample_request_listFunction(){
	hideCustomerFunction();
	document.getElementById('sample_request_list').style.display = 'block';

}

function hold_request_listFunction(){
	hideCustomerFunction();
	document.getElementById('hold_request_list').style.display = 'block';
}

//officer
function hideOfficerFunction(){

	document.getElementById('intro_officer').style.display = 'none';
	document.getElementById('registerProcess_list').style.display = 'none';
	document.getElementById('modify_registerProcess_list').style.display = 'none';
	document.getElementById('extend_registerProcess_list').style.display = 'none';
	document.getElementById('substitue_registerProcess_list').style.display = 'none';
	document.getElementById('substitue_registerProcess_list').style.display = 'none';
	document.getElementById('sampleProduceProcess_list').style.display = 'none';
	document.getElementById('sampleImportProcess_list').style.display = 'none';
	document.getElementById('holdProcess_list').style.display = 'none';
	document.getElementById('modify_holdProcess_list').style.display = 'none';
	document.getElementById('extend_registerProcess_list').style.display = 'none';
	document.getElementById('substitue_holdProcess_list').style.display = 'none';
	document.getElementById('holdProcess_list').style.display = 'none';
	document.getElementById('modify_holdProcess_list').style.display = 'none';
	document.getElementById('extend_registerProcess_list').style.display = 'none';
	document.getElementById('substitue_holdProcess_list').style.display = 'none';

}

function registerFunction(){
	hideOfficerFunction();
	document.getElementById('registerProcess_list').style.display = 'block';
}

function modify_registerFunction(){
	hideOfficerFunction();
	document.getElementById('modify_registerProcess_list').style.display = 'block';
}

function extend_registerFunction(){
	 hideOfficerFunction();
	  document.getElementById('extend_registerProcess_list').style.display = 'block';
}


function substitue_registerFunction(){

	hideOfficerFunction();
 	 document.getElementById('substitue_registerProcess_list').style.display = 'block';
}

function sampleProduceFunction(){
	hideOfficerFunction();
	document.getElementById('sampleProduceProcess_list').style.display = 'block';

}

function sampleImportFunction(){
	hideOfficerFunction();
	document.getElementById('sampleImportProcess_list').style.display = 'block';

}

function holdFunction(){
	hideOfficerFunction();	
	document.getElementById('holdProcess_list').style.display = 'block';
}

function modify_holdFunction(){
	hideOfficerFunction();
	document.getElementById('modify_holdProcess_list').style.display = 'block';
}

function extend_holdFunction(){
	hideOfficerFunction();
	document.getElementById('extend_registerProcess_list').style.display = 'block';
}

function substitue_holdFunction(){
	hideOfficerFunction();
	document.getElementById('substitue_holdProcess_list').style.display = 'block';
}