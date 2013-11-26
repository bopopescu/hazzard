


function validate()
{
}

/*
*  start checking form
*/

validate.prototype.resultCheck = true;

validate.prototype.start = function() {
	// list input that must be text
	var textOnly = ["nameBox","regionBox","name_storage","name_manufacture","specialistBox","specialist2","departmentBox","ministryBox","toBox","official_nameBox","producer_nameBox","importer_nameBox"
					,"package_nameBox","type_usingBox","producerBox","countryBox"];

    var resultTxt = [];
    //list inut that must be integer
    var IntegerOnly = ["mobile_contactBox","fax_contactBox","zip_contactBox","code_taxBox",
    					"zip_storage","zip_manufacture","mobile_storage","mobile_manufacture","fax_storage","fax_manufacture"
    					,"codeBox","maxArea_storage","orderBox","hazard_number_contactBox","hazard_mo_contactBox"
    					,"hazard_zip_contactBox","hazard_mobile_contactBox","hazard_fax_contactBox","typeBox","quantity_nameBox","yearBox2","dayBox2"
    					,"monthBox2","ageBox","extend_doc_number"];
    var resultInt = [];

    
    var cantNull = ["address_contactBox","address_storage","address_manufacture","hazardous_nameBox","marketingBox","descriptionBox","reasonArea","hazardousBox","formulaBox"
    				,"conditionBox","quantityBox","solution_nameBox","officialBox","seller_nameBox"];
    // values in every input
    var canNull = ["fax_contactBox","hazard_fax_contactBox","fax_storage","fax_manufacture"];

    var resultAddr = [];
    //start getData
    this.getData(resultInt,IntegerOnly,resultTxt,textOnly,cantNull,resultAddr,canNull);

    return this.resultCheck;
};

/*
	get data from input by getElementById
	@param resultInt array for store all value from each input
	@param IntegerOnly list of id in each input
	@param 
*/
validate.prototype.getData = function(resultInt,IntegerOnly,resultTxt,textOnly,addressList,resultAddr,canNull)
{     
    var newIntegerOnly =[];
    var newTextOnly = [];
    var newAddrList = [];
    var newNull = [];

    var newResultInt = [];
    var newResultTxt = [];
    var newResultAddr = [];
    var newResultNull = [];
	for(var i = 0; i < IntegerOnly.length ; i++)
	{    
		 if($('#'+IntegerOnly[i]).val() === undefined)
		 {  
   				this.message("Not found this id " + IntegerOnly[i]);
    	}
    	else if($('#'+IntegerOnly[i]).val() || $('#'+IntegerOnly[i]).val().length == 0)
    	{
    		newResultInt[newResultInt.length] = $('#'+IntegerOnly[i]).val();
    		newIntegerOnly[newIntegerOnly.length] = IntegerOnly[i];
    	}
	}

	for(var i = 0; i < textOnly.length ; i++)
	{	
		if($('#'+textOnly[i]).val()  === undefined){
			this.message("Not found this id " + textOnly[i]);
		}
		else if( $('#'+textOnly[i]).val() || $('#'+textOnly[i]).val().length == 0){
    		newResultTxt[newResultTxt.length] = $('#'+textOnly[i]).val();
    		newTextOnly[newTextOnly.length] = textOnly[i];
    	}
	}

	for(i = 0; i < addressList.length ; i++)
	{	
		if($('#'+addressList[i]).val() === undefined)
		{
			this.message("Not found this id " + addressList[i]);
		}
		else if($('#'+addressList[i]).val() || $('#'+addressList[i]).val().length == 0){
    		newResultAddr[newResultAddr.length] = $('#'+addressList[i]).val();
    		newAddrList[newAddrList.length] = addressList[i];
    	}
	}


	//resultInt = this.eliminateDuplicates(resultInt);
	//resultTxt = this.eliminateDuplicates(resultTxt);
	//resultAddr = this.eliminateDuplicates(resultAddr);

	this.startCheck(newResultInt,newIntegerOnly,newResultTxt,newTextOnly,newAddrList,newResultAddr,canNull);

}

validate.prototype.startCheck = function(resultInt,IntegerOnly,resultTxt,textOnly,addressList,resultAddr,canNull)
{   
	var errorId = [];
	var errorIdNum = 0;

	for(i = 0; i < IntegerOnly.length ; i++)
	{	    
			console.log(IntegerOnly[i]);
		    var intRegex = /^\d+$/;
		    var canNullButNovalue = false;
		    console.log($.inArray(IntegerOnly[i],canNull)+ " -------------> > > = " + IntegerOnly[i]);

		    if(resultInt[i].length == 0 && $.inArray(IntegerOnly[i],canNull) != -1)
		    {
		    	canNullButNovalue = true;
		    }

		    if(resultInt[i].length == 0 && $.inArray(IntegerOnly[i],canNull) == -1){
		    	this.message("Empty value at " + IntegerOnly[i]);
		    	errorId[errorIdNum] = IntegerOnly[i];
				errorIdNum++;
				this.resultCheck = false;
		    }
			else if(intRegex.test(resultInt[i]) || canNullButNovalue) {
			   	this.message(resultInt[i] + "  Pass");
			   	this.handlePass(IntegerOnly[i]);
			}
			else
			{
				this.message(resultInt[i] + "  Error");	
				errorId[errorIdNum] = IntegerOnly[i];
				errorIdNum++;
				this.resultCheck = false;
			}
	}

	for(i = 0; i < textOnly.length ; i++)
	{		
		var rexText = /^\D+$/;
		if(resultTxt[i].length == 0 && $.inArray(IntegerOnly[i],canNull) == -1){
			this.message("Empty value at " + textOnly[i]);
			errorId[errorIdNum] = textOnly[i];
			errorIdNum++;
			this.resultCheck = false;
		}
		else if(rexText.test(resultTxt[i]))
		{
			this.message(resultTxt[i] + " Pass");
			this.handlePass(textOnly[i]);
		}
		else
		{
			this.message(resultTxt[i] + " Error");
			errorId[errorIdNum] = textOnly[i];
				errorIdNum++;
				this.resultCheck = false;
		}
	}

	for(i = 0; i < addressList.length ; i++)
	{
		if(resultAddr[i].length == 0){
			this.message("Empty value at " + addressList[i]);
			errorId[errorIdNum] = addressList[i];
			errorIdNum++;
			this.resultCheck = false;
		}
		else
		{
			this.message(resultAddr[i] + " Pass");	
			this.handlePass(addressList[i]);
		}
	}

	this.messageError(errorId);

}

validate.prototype.handlePass = function(passId){
	document.getElementById(passId).style.background = "#FAFAFA";
}

validate.prototype.messageError = function(errorList){
	if(errorList.length != 0)
	{
		this.showError(errorList);
	}

}

validate.prototype.showError = function(errorList){
	for(var i = 0 ; i < errorList.length ; i++)
	{
		document.getElementById(errorList[i]).style.background = "#FF6347";
		this.message("Show at " +  errorList[i]);
	}
}

validate.prototype.message = function(message){
	console.log(message);
}

validate.prototype.eliminateDuplicates =  function(arr){
var i,
  len=arr.length,
  out=[],
  obj={};

 for (i=0;i<len;i++) {
 obj[arr[i]]=0;
 }
 for (i in obj) {
 out.push(i);
 }
 return out;
}

validate.prototype.removeData = function(arr,i){

	var index = arr.indexOf(arr[i]);
			if (index > -1) {
		    arr.splice(index, 1);
			}

			return arr;
}

