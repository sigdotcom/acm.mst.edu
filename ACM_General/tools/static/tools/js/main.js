var data = {}
jQuery.getJSON("/web-api/accounts/?format=json", function generate_table(data) {
  CreateAccountsTable ( data ) ;
})

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
    var statusText = document.createTextNode((data[i].is_active?'':'in')+"active");
    status.appendChild(statusText);    

    //create setting table data cell
    var settings = document.createElement("td");
    //create delete button
    var deleteButton = document.createElement("a");
    deleteButton.href="";
    var deleteButtonIconContainer = document.createElement("i");
    deleteButtonIconContainer.classList.add("material-icons");
    var deleteButtonIcon = document.createTextNode("delete");
    //create edit button
    var editButton = document.createElement("a");
    editButton.href="";
    var editButtonIconContainer = document.createElement("i");
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
