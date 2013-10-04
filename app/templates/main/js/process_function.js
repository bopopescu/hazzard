
function register_request_listFunction(){

	var el = document.getElementById('register_request_list');
	el.style.visibility = 'visible';
	
	var ch = document.getElementById('modify_link');
	ch.setAttribute("href", "modify_register_request_customer.html");


	var mn = document.getElementById('extend_link');
	mn.setAttribute("href","extend_register_request_customer.html");
	
}

// function modify_register_request_listFunction(){

// 	var el = document.getElementById('modify_register_request_list');
// 	el.style.visibility = 'visible';
	
// 	var ch = document.getElementById('modify_link');
// 	ch.setAttribute("href", "modify_register_request_customer.html");


// 	var mn = document.getElementById('extend_link');
// 	mn.setAttribute("href","extend_register_request_customer.html");
	
// }

// function extend_register_request_listFunction(){

// 	var el = document.getElementById('extend_register_request_list');
// 	el.style.visibility = 'visible';
	
// 	// var ch = document.getElementById('modify_link');
// 	// ch.setAttribute("href", "modify_register_request_customer.html");


// 	var mn = document.getElementById('extend_link');
// 	mn.setAttribute("href","extend_register_request_customer.html");
	
// }

function substitute_register_request_listFunction(){

	var el = document.getElementById('substitute_register_request_list');
	el.style.display = '';
	
	// var ch = document.getElementById('modify_link');
	// ch.setAttribute("href", "modify_register_request_customer.html");


	// var mn = document.getElementById('extend_link');
	// mn.setAttribute("href","extend_register_request_customer.html");
	
}

//officer
function registerFunction(){

	
	
	document.getElementById('intro_officer').style.display = 'none';
	document.getElementById('registerProcess_list').style.display = 'block';
	 document.getElementById('modify_registerProcess_list').style.display = 'none';
	 document.getElementById('extend_registerProcess_list').style.display = 'none';



	
	// var list_Title = document.getElementById("list_Title");
	// list_Title.innerHTML='รายชื่อผู้ชื่อ ผู้ขอใบขึ้นทะเบียนวัตถุอันตราย';

	// var ch = document.getElementById('check_value_link');
	// ch.setAttribute("href", "register_request_view_officer.html");


	// var mn = document.getElementById('manage_value_link');
	// mn.setAttribute("href","register_permit_officer.html");
	

}

function modify_registerFunction(){

	document.getElementById('intro_officer').style.display = 'none';
	 document.getElementById('modify_registerProcess_list').style.display = 'block';
	 document.getElementById('registerProcess_list').style.display = 'none';
	 document.getElementById('extend_registerProcess_list').style.display = 'none';



	// var list_Title = document.getElementById("list_Title");
	// list_Title.innerHTML='รายชื่อผู้ประการที่ขออนญาตเปลี่ยนแปลงข้อมูลใน ใบอนุญาตขึ้นทะเบียนวัตถุอันตราย';

	// var ch = document.getElementById('check_value_link');
	// ch.setAttribute("href", "modify_register_request_customer.html");

	// var mn = document.getElementById('manage_value_link');
	// mn.setAttribute("href","modify_register_permit_officer.html");
			
    
}

function extend_registerFunction(){
	document.getElementById('intro_officer').style.display = 'none';
	 document.getElementById('modify_registerProcess_list').style.display = 'none';
	 document.getElementById('registerProcess_list').style.display = 'none';
	  document.getElementById('extend_registerProcess_list').style.display = 'block';


	 


	// var list_Title = document.getElementById("list_Title");
	// list_Title.innerHTML='รายชื่อผู้ประการที่ขออนญาตต่ออายุ ใบอนุญาตขึ้นทะเบียนวัตถุอันตราย'
			
 //    var ch = document.getElementById('check_value_link');
	// ch.setAttribute("href", "extend_register_request_customer.html");

	// var mn = document.getElementById('manage_value_link');
	// mn.setAttribute("href","extend_register_permit_officer.html");
    
}


function substitue_registerProcess_list(){
	document.getElementById('intro_officer').style.display = 'none';
	 document.getElementById('substitue_registerProcess_list').style.display = 'block';
	 document.getElementById('registerProcess_list').style.display = 'none';

}
