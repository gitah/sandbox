/*
 * word-replace.js: 
 * Preforms find and replace text for all Word Documents of a given folder
 * NOTE: Requires Windows Script Host to run
 * 2011-03-25
 *
 * By Fred Song, xx@uvic.ca
 * Public Domain.
 * NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
 */


/*--------CONFIGURATION---------*/
fileExpr = /(.)*\.docx?/i;

/* Change this section! */
folderPath = "C:/your/directory"; 	//Folder Path
oldText = "hi" 	   					//String to find!
newText = "Hello" 					//Replace with!
/*--------------------------------*/

(function() {
    //Word ActiveX object
    var objWord = new ActiveXObject('Word.Application'); 	
    objWord.Visible = false;

    //Get all files (non recursive) in the given folder
    var files = getFolderFiles(folderPath);

    //For all Word files, replace all instances of oldText with newText
    var currFileName;
    for(var i=0; i<files.length; i++) {
        currFileName = files[i];

        if(fileExpr.test(currFileName)) {
            replaceTextWordDoc(currFileName, oldText, newText);
        }
    }
    
    objWord.Quit();
}());

//-- Helper Functions --//
/* Returns an array with the file names of a folder (No recursion into subfolders) */
function getFolderFiles(folderPath) {
    var fso, folder, fc, files, fileName;

    fso = new ActiveXObject("Scripting.FileSystemObject");

    folder = fso.GetFolder(folderPath);
    fc = new Enumerator(folder.files);

    files = [];

    for (; !fc.atEnd(); fc.moveNext()) {
        fileName = '' + fc.item();
        files.push(fileName);
    }

    return files;
}



/* Replaces all instances of oldStr with newStr for the Word Document provided */
function replaceTextWordDoc(docPath, oldStr, newStr) {
    var doc = objWord.Documents.Open(docPath);	

    //Get document contents
    var range = doc.Content;

    //Replace command (http://msdn.microsoft.com/en-us/library/ms250450%28v=Office.11%29.aspx)
    var wdReplaceAll = 2;
    var wdFindContinue = 1;
    range.Find.Execute(oldStr,			//Find Text
                       false,			//Match Case
                       false,			//Match Whole Word
                       false,			//Match Wild Cards
                       false,			//Match Sounds Like
                       false,			//Match All Word Forms
                       false,			//Forward
                       wdFindContinue,	//Wrap
                       false,			//Format
                       newStr,			//Replace With
                       wdReplaceAll,	//Replace
                       false,			//Match Kashida
                       false,			//Match Diacritics
                       false,			//Match Alef Hamza
                       false);			//Match Control

    doc.Close();
}


/* References 

	http://msdn.microsoft.com/en-us/library/aa221371%28office.11%29.aspx
	http://msdn.microsoft.com/en-us/library/aa196075%28v=office.11%29.aspx
	http://msdn.microsoft.com/en-us/library/aa223066%28v=office.11%29.aspx
	http://msdn.microsoft.com/en-us/library/aa221467%28v=office.11%29.aspx

	http://stackoverflow.com/questions/768260/replace-text-in-word-document-with-activex
*/
