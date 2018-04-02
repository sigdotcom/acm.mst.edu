alert(data);
alert("in search");

const SEARCH_BAR_ID = "SearchBar" ;
const ACCOUNTS_TABLE_ID = "AccountsTable" ;
const EMPTY_TEXT = "" ;
const SPACE_LETTER = " " ;

function RetrieveText ( InputElement )
{
  var InputText = InputElement . value ;
  return InputText ;
}

function RetrieveElement ( InputId )
{
  var Element = document . getElementById ( InputId ) ;
  return Element ;
}

function RetrieveSearchText ( )
{
  var SearchBar = RetrieveElement ( SEARCH_BAR_ID ) ;
  var SearchText = RetrieveText ( SearchBar )
  return SearchText ;
}

function ClearElement ( Element )
{
  Element . innerHTML = EMPTY_TEXT ;
}

function RetrieveAccountsTable ( )
{
  var AccountsTable = RetrieveElement ( ACCOUNTS_TABLE_ID ) ;
  return AccountsTable ;
}

function ClearListOfAccounts ( )
{
  var AccountsTable = RetrieveAccountsTable ( ) ;
  ClearElement ( AccountsTable ) ;
}

function FuzzySearch ( Haystack , Needle )
{
  var DoesContain = false ;
  var PositionAt = Haystack . search ( Needle ) ;
  if ( PositionAt != -1 )
  {
    DoesContain = true ;
  }
  return DoesContain ;
}

function FuzzySearchRow ( Row , SearchText )
{
  var IsGood = false ;
  var FirstName = Row . first_name ;
  var LastName = Row . last_name ;
  var Name = FirstName + SPACE_LETTER + LastName ;
  var EmailAddress = Row . email ;
  var Activeness = Row . is_active ;
  var LowerCaseName = Name . toLowerCase ( ) ;
  var LowerCaseEmailAddress = EmailAddress . toLowerCase ( ) ;
  var LowerCaseActiveness = Activeness . toLowerCase ( ) ;
  
  var IsGoodInName = FuzzySearch ( LowerCaseName , SearchText ) ;
  var IsGoodInEmail = FuzzySearch ( LowerCaseEmailAddress , SearchText ) ;
  var IsGoodInActiveness = FuzzySearch ( LowerCaseActiveness , SearchText ) ;
  if ( IsGoodInName == true || IsGoodInEmail == true || IsGoodInActiveness == true )
  {
    IsGood = true ;
  }
  return IsGood ;
}

function FuseSearchFilter ( FullData , SearchText )
{
  var options = {
    shouldSort: true,
    threshold: 0.6,
    location: 0,
    distance: 100,
    maxPatternLength: 32,
    minMatchCharLength: 1,
    keys: [
      "first_name",
      "last_name",
      "email",
      "is_active"
  ]
  };
  var fuse = new Fuse(FullData, options); // "list" is the item array
  var result = fuse.search(SearchText);
  var FilteredData = result ;
  return FilteredData ;
}

/*
function SearchFilter ( FullData , SearchText )
{
  var LowerCaseSearchText = SearchText . toLowerCase ( ) ;
  var FilteredData = [ ] ;
  var FullDataLength = FullData . length ;
  var FullDataIndex = 0 ;
  while ( FullDataIndex < FullDataLength )
  {
    var Row = FullData [ FullDataIndex ] ;
    var IsGood = FuzzySearchRow ( Row , LowerCaseSearchText ) ;
    if ( IsGood == true )
    {
      FilteredData . push ( Row ) ;
    }
    FullDataIndex = FullDataIndex + 1 ;
  }
  return FilteredData ;
}
*/

function SearchFunction ( )
{
  var SearchText = RetrieveSearchText ( ) ;
  ClearListOfAccounts ( ) ;
  var FilteredData = FuseSearchFilter ( data , SearchText ) ;
  var AccountsTable = RetrieveAccountsTable ( ) ;
  PopulateAccountsTable ( FilteredData , AccountsTable ) ;
}
