
//customer
function hideCustomerFunction(){
	document.getElementById('intro_officer').style.display = 'none';
	document.getElementById('register_request_list').style.display = 'none';
	document.getElementById('sample_request_list').style.display = 'none';
	document.getElementById('hold_request_list').style.display = 'none';
	document.getElementById('import_request_list').style.display = 'none';
	document.getElementById('export_request_list').style.display = 'none';
	document.getElementById('produce_request_list').style.display = 'none';
	



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

function import_request_listFunction(){
	hideCustomerFunction();
	document.getElementById('import_request_list').style.display = 'block';
}

function export_request_listFunction(){
	hideCustomerFunction();
	document.getElementById('export_request_list').style.display = 'block';
}

function produce_request_listFunction(){
	hideCustomerFunction();
	document.getElementById('produce_request_list').style.display = 'block';
}

//officer
function hideOfficerFunction(){

	document.getElementById('intro_officer').style.display = 'none';
	document.getElementById('registerProcess_list').style.display = 'none';
	document.getElementById('modify_registerProcess_list').style.display = 'none';
	document.getElementById('extend_registerProcess_list').style.display = 'none';
	document.getElementById('substitue_registerProcess_list').style.display = 'none';

	document.getElementById('sampleProduceProcess_list').style.display = 'none';
	document.getElementById('sampleImportProcess_list').style.display = 'none';

	document.getElementById('holdProcess_list').style.display = 'none';
	document.getElementById('modify_holdProcess_list').style.display = 'none';
	 document.getElementById('extend_holdProcess_list').style.display = 'none';
	document.getElementById('substitue_holdProcess_list').style.display = 'none';

	document.getElementById('importProcess_list').style.display = 'none';
	document.getElementById('modify_importProcess_list').style.display = 'none';
	 document.getElementById('extend_importProcess_list').style.display = 'none';
	document.getElementById('substitue_importProcess_list').style.display = 'none';

	document.getElementById('exportProcess_list').style.display = 'none';
	document.getElementById('modify_exportProcess_list').style.display = 'none';
	 document.getElementById('extend_exportProcess_list').style.display = 'none';
	document.getElementById('substitue_exportProcess_list').style.display = 'none';

	document.getElementById('produceProcess_list').style.display = 'none';
	document.getElementById('modify_produceProcess_list').style.display = 'none';
	 document.getElementById('extend_produceProcess_list').style.display = 'none';
	document.getElementById('substitue_produceProcess_list').style.display = 'none';

	document.getElementById('report_person').style.display = 'none';
	document.getElementById('report_country').style.display = 'none';
	document.getElementById('report_placeKeep').style.display = 'none';
	document.getElementById('report_name').style.display = 'none';
	document.getElementById('report_log').style.display = 'none';

	

	
	
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
	document.getElementById('extend_holdProcess_list').style.display = 'block';
}

function substitue_holdFunction(){
	hideOfficerFunction();
	document.getElementById('substitue_holdProcess_list').style.display = 'block';
}

function importFunction(){
	hideOfficerFunction();
	document.getElementById('importProcess_list').style.display = 'block';

}

function modify_importFunction(){
	hideOfficerFunction();
	document.getElementById('modify_importProcess_list').style.display = 'block';
}

function extend_importFunction(){
	hideOfficerFunction();
	document.getElementById('extend_importProcess_list').style.display = 'block';
}

function substitue_importFunction(){
	hideOfficerFunction();
	document.getElementById('substitue_importProcess_list').style.display = 'block';

}


function exportFunction(){
	hideOfficerFunction();
	document.getElementById('exportProcess_list').style.display = 'block';

}

function modify_exportFunction(){
	hideOfficerFunction();
	document.getElementById('modify_exportProcess_list').style.display = 'block';
}

function extend_exportFunction(){
	hideOfficerFunction();
	document.getElementById('extend_exportProcess_list').style.display = 'block';
}

function substitue_exportFunction(){
	hideOfficerFunction();
	document.getElementById('substitue_exportProcess_list').style.display = 'block';

}

function produceFunction(){
	hideOfficerFunction();
	document.getElementById('produceProcess_list').style.display = 'block';

}

function modify_produceFunction(){
	hideOfficerFunction();
	document.getElementById('modify_produceProcess_list').style.display = 'block';
}

function extend_produceFunction(){
	hideOfficerFunction();
	document.getElementById('extend_produceProcess_list').style.display = 'block';
}

function substitue_produceFunction(){
	hideOfficerFunction();
	document.getElementById('substitue_produceProcess_list').style.display = 'block';

}

function reportPersonFunction(){
	hideOfficerFunction();
	document.getElementById('report_person').style.display = 'block';
}

function reportCountryFunction(){
	hideOfficerFunction();
	document.getElementById('report_country').style.display = 'block';
}

function reportPlaceFunction(){
	hideOfficerFunction();
	document.getElementById('report_placeKeep').style.display = 'block';
}


function reportNameFunction(){
	hideOfficerFunction();
	document.getElementById('report_name').style.display = 'block';

}

function reportLogFunction(){
	hideOfficerFunction();
	document.getElementById('report_log').style.display = 'block';
}

	
function queryperson(){
	// hideOfficerFunction();
	document.getElementById('table_person').style.display = 'block';
}

function querycountry(){
	// hideOfficerFunction();
	document.getElementById('table_country').style.display = 'block';
}

function queryplace(){
	// hideOfficerFunction();
	document.getElementById('table_place').style.display = 'block';
}
	

function queryname(){
	// hideOfficerFunction();
	document.getElementById('table_name').style.display = 'block';
}
	
function querylog(){
	// hideOfficerFunction();
	document.getElementById('table_log').style.display = 'block';
}
	


