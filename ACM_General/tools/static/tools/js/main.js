jQuery.getJSON("/web-api/accounts/?format=json", (data) => CreateAccountsTable(data));
function CreateAccountsTable ( data )
{
  var body = document.getElementsByClassName("container")[0];

  var tbl = document.createElement("div");
  tbl.setAttribute("id", "AccountsTable");
  tbl.classList.add("table");
  tbl.classList.add("table-striped");
  tbl.classList.add("table-hover");
  tbl.style.display="table";
  
  body.appendChild(tbl);
  
  PopulateAccountsTable ( data , tbl ) ;
}

function PopulateAccountsTable ( data , tbl )
{
  //Create Header
  var tblHead = document.createElement("thead");
  var nameHead = document.createElement("th");
  var nameHeadText = document.createTextNode('Name');
  nameHead.appendChild(nameHeadText);
  var emailHead = document.createElement("th");
  var emailHeadText = document.createTextNode('Email');
  emailHead.appendChild(emailHeadText);
  var statusHead = document.createElement("th");
  var statusHeadText = document.createTextNode('Status');
  statusHead.appendChild(statusHeadText);
  var settingsHead = document.createElement("th");
  var settingsHeadText = document.createTextNode('');
  settingsHead.appendChild(settingsHeadText);

  tblHead.appendChild(nameHead);
  tblHead.appendChild(emailHead);
  tblHead.appendChild(statusHead);
  tblHead.appendChild(settingsHead);

  var tblBody = document.createElement("tbody");

  // creating all cells
  for (let i in data) {
    // --creates a table row--
    var row = document.createElement("tr");
    row.id = "row-" + data[i].id;
    row.classList.add((data[i].is_active?"success":"warning"));

    //create and fill name column table data cell
    var name = document.createElement("td");
    var nameText = document.createTextNode(data[i].first_name+' '+data[i].last_name);
    name.appendChild(nameText);
    //create and fill email column table data cell
    var email = document.createElement("td");
    var emailText = document.createTextNode(data[i].email);
    email.appendChild(emailText);
    //create and fill status table data cell
    var status = document.createElement("td");
    status.id = "status_cell-" + data[i].id;
    var statusText = document.createTextNode((data[i].is_active?'':'in')+"active");
    status.appendChild(statusText);    

    //create setting table data cell
    var settings = document.createElement("td");
    //create delete button
    var deleteButton = document.createElement("button");
    let butId = "but-" + data[i].id;
    deleteButton.id = butId;
    deleteButton.setAttribute('onclick', 'deleteEntry(\"'+butId+'\")');
    deleteButton.classList.add("material-icons");
    var deleteButtonIconContainer = document.createElement("a");
    var deleteButtonIcon = document.createTextNode("delete");
    //create edit button
    var editButton = document.createElement("a");
    var editButtonIconContainer = document.createElement("a");
    editButtonIconContainer.classList.add("material-icons");
    var editButtonIcon = document.createTextNode("build");


    //adds created table data to row
    editButtonIconContainer.appendChild(editButtonIcon);
    editButton.appendChild(editButtonIconContainer);
    settings.appendChild(editButton);
    deleteButtonIconContainer.appendChild(deleteButtonIcon);
    deleteButton.appendChild(deleteButtonIconContainer);
    settings.appendChild(deleteButton);
    row.appendChild(name);
    row.appendChild(email);
    row.appendChild(status);
    row.appendChild(settings);

    tblBody.appendChild(row);
  }

  // put the <tbody> in the <table>
  tbl.appendChild(tblHead);
  var hr = document.createElement("hr");
  tbl.appendChild(hr);
  tbl.appendChild(tblBody);
  // appends <table> into <body>
}

// deletes a person/row in the database
// there is no true deletion, the active attribute is just set to false
function deleteEntry(buttonId) {
  buttonId = buttonId.replace("but-","");
  urltext = "/web-api/accounts/" + buttonId + "/"
  
  //edit database to "delete" entry
  let row = document.getElementById("row-" + buttonId);
  if (row.classList.contains("success")){
    answer = false;
  }
  else{
    answer = true;
  }

  $.ajax({
    url: urltext,
    dataType: 'json',
    type: 'patch',
    contentType: 'application/json',
    data: JSON.stringify({"is_active": answer}),
  }).done(function(){console.log("yep")}).fail(function(a,b,c){console.log("nope",a,b,c)});


  
  
  //change the status column cell to show result of change
  document.getElementById("status_cell-"+buttonId).innerHTML = (!(row.classList.contains("success"))?'':'in')+"active";
  //change row color to signify successfull deletion(change of attribute)
  if (row.classList.contains("success")){
    row.classList.remove("success");
    row.classList.add("warning");
  }
  else{
    row.classList.remove("warning");
    row.classList.add("success");
  }   
}