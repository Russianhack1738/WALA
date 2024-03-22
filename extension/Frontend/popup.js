document.getElementById("convert").addEventListener("click",convertCheckboxValues)
hideSpinner();

function formatValue(value) {
  // Check if the value is a number before using toFixed
  return typeof value === 'number' ? value.toFixed(2) : value;
}

function showSpinner() {
    const spinner = document.querySelector('.spinner-border');
    spinner.style.display = 'inline-block';  // Show the spinner
}

function hideSpinner() {
    const spinner = document.querySelector('.spinner-border');
    spinner.style.display = 'none';  // Hide the spinner
}

function getCurrentTabUrl(callback) {  
    var queryInfo = {
      active: true, 
      currentWindow: true
    };
  
    chrome.tabs.query(queryInfo, function(tabs) {
      var tab = tabs[0]; 
      var url = tab.url;
      callback(url);
    });
}

function convertCheckboxValues(){
	const block1 = document.getElementById("output");
	const block2 = document.getElementById("output1");
	block1.style.display = "none";
	block2.style.display = "none";
    var values = [];
chrome.tabs.query({'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT},
   function(tabs){
    values.push(tabs[0].url);
	showSpinner();  // Show spinner before fetching data
    buttonSend(values);
   });
}

function printData(data)
{	
	const block1 = document.getElementById("output");
	const block2 = document.getElementById("output1");
	block2.style.display = "block";
    const resul1 = document.getElementById('output1');
    let values = Object.values(data);
    let keys = Object.keys(data)
	hideSpinner();  // Hide spinner after data is received
	resul1.innerHTML = "<strong>" + keys[0] + ":</strong> " + formatValue(values[0]) + "<br />" +
                   "<strong>" + keys[1] + ":</strong> " + formatValue(values[1]) + "<br />" +
                   "<strong>" + keys[2] + ":</strong> " + formatValue(values[2]) + "<br />" +
                   "<strong>" + keys[3] + ":</strong> " + formatValue(values[3]) + "<br />" +
                   "<strong>" + keys[4] + ":</strong> " + formatValue(values[4]) + "<br><br><p><strong>Autism Friendliness Status:</strong> Bad</p>"	;
    console.log(data);
}

function buttonSend(values)
{   
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
      values.push(checkbox.checked);
    });

    var res="";
    const resul = document.getElementById('output');
    const resul1 = document.getElementById('output1');
    resul.textContent = JSON.stringify(values);

    fetch('http://127.0.0.1:5000/scan?data1='+values[0]+'&data2='+values[1]+'&data3='+values[2]+'&data4='+values[3]+'&data5='+values[4]+'&data6='+values[5], {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
})
.then(response => response.json())
.then(data => printData(data))
    .catch(error => {
        hideSpinner();  // Hide spinner in case of an error
        console.error('Error:', error);
    });
}
           
