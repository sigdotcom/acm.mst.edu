var data = {}
jQuery.getJSON("/web-api/accounts/?format=json", function generate_table(data) {
  CreateAccountsTable ( data ) ;
}

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
    // creates a table row
    var row = document.createElement("tr");
    row.classList.add((data[i].is_active?"success":"warning"));
    var name = document.createElement("td");
    var nameText = document.createTextNode(data[i].first_name+' '+data[i].last_name);
    name.appendChild(nameText);
    var email = document.createElement("td");
    var emailText = document.createTextNode(data[i].email);
    email.appendChild(emailText);
    var status = document.createElement("td");
    var statusText = document.createTextNode((data[i].is_active?'':'in')+"active");
    status.appendChild(statusText);
    var settings = document.createElement("td");
    var settingsButton = document.createElement("a");
    settingsButton.href="";
    var settingsButtonIconContainer = document.createElement("i");
    settingsButtonIconContainer.classList.add("material-icons");
    var settingsButtonIcon = document.createTextNode("settings");

    settingsButtonIconContainer.appendChild(settingsButtonIcon);
    settingsButton.appendChild(settingsButtonIconContainer);
    settings.appendChild(settingsButton);
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
