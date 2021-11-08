
<div id="top"></div>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#getting-the-csv-file">Getting the CSV file</a></li>
        <li><a href="#quick-start-guide">Quick Start Guide</a></li>
      </ul>
    </li>
    <li><a href="#settings.json">settings.json</a></li>
    <li>
     <a href="#google-sheets">Google Sheets</a>
      <ul>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#client_key.json">client_key.json</a></li>
       </ul>
      </li>
      <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started
Script to automatically partition the grading of a Gradescope assignment. Can output the partition to a txt file, a json file, or to a google sheet.

### Prerequisites

Python 3+ Required

### Getting the CSV File

Go to the assignment page on Gradescope, then click
Review Grades -> Download Grades (Located at the bottom of the page)
->Download CSV

### Quick Start Guide

1. Clone the repo
   ```sh
   git clone https://github.com/Ryguy924/Grading-Partition.git
   ```
   OR
   Copy all .py files into a directory
   
2. If you do not have <a href="#settings.json">settings.json</a> configured, run
   ```sh
   python3 main.py setup
   ```
   and view the documentation on how to configure settings.json.
3. Once settings.json  is setup, run
   ```sh
   python3 main.py "filepath_to_csv"
   ```
   for example
    ```sh
   python3 main.py ./Assignment_7_Scores.csv
   ```
   After this, a new file called partition.txt or partition.json will be created in the directory depending on the output method specified. That file will contain the partition.
   If you are using <a href="#google-sheets">Google Sheets</a>, a spreadsheet will be created instead of a partition file.


<!-- USAGE EXAMPLES -->
## settings.json

settings.json is a file located in the directory of the .py files that holds most information, such as instructor names, how many hours each instructor works or should dedicate to grading, and how the partition should be outputted.

### "instructors"
Dictionary of instructor names to how many hours they work.
For example:
```json
"instructors":{
        "BOB SMITH": 20,
        "SARAH":10
    }
```
Note that grading amount is relative, so if we changed Bob to 10 and Sarah to 5 it would result in the same amount of grading. 

Also, if the instructor's name matches how it appears in Gradescope, their submissions will be ignored and not partitioned to any instructor.

### "output"
How the partition should be outputted. 
Possible values for this field are:

 - "txt" Output partition into a readable text file.
 - "json" Output partition into a json file.
 - "googlesheets" Create a spreadsheet for the partition. <a href="#google-sheets">Please refer to the documentation on creating a spreadsheet</a> before using.

### "sheetUrl"
This field is only required if the "output" field is set to "googlesheets"

Specifies the url of the google sheet to create the partition on.


## Google Sheets
There is optional functionality to output the partition onto a google sheet.
Run this command to install the required libraries.
  ```sh
   pip3 install gspread oauth2client
   ```

### Usage
If you do not have <a href="#client_key.json">client_key.json</a> setup, you will need to set it up prior to these instructions.

Inside client_key.json, there is a "service_email" field. Copy the email, and share the google sheet you wish to use to this email. Make sure it has editor permissions.

Copy the url of the google sheet you wish to use into a "sheetUrl" field in settings.json. For example:
```json
"instructors":{
        "BOB SMITH": 20,
        "SARAH":10
    }, 
"output":"googlesheets",

"sheetUrl":"https://docs.google.com/spreadsheets/d/boguslink"
```

After running the <a href="#quick-start-guide">script</a>, a new worksheet called "New Assignment" will be created with the partition. 
NOTE: Before running the script again, you must either rename or delete this worksheet.


### client_key.json
This is a file required in the same directory as the .py files if you wish to use the google sheets functionality. There is some Google API setup required, you only have to do this once.

 1. Visit [https://console.developers.google.com/](https://console.developers.google.com/)
 2. Create a new Project <img src="https://drive.google.com/uc?export=view&id=16aIkntgwlSiOdUZxOhbqgEIC_r0UOrYN"> 
 3. Once the project is created, click on "Enable API's and Services". Search for the Google Sheets API and the Google Drive API and enable both. If you need to get back to the API menu after enabling one of them, click on the "API's and Services" menu here: <img src="https://drive.google.com/uc?export=view&id=1PCXx8Huvd391VA6OGqokCnoMplydirhn"> 
 4. Create a new credential from the Credentials menu. I recommend the "help me choose" option. <img src="https://drive.google.com/uc?export=view&id=1oTRA8TAaYxWFHl1U8Ee9aSB14GcMYTWJ"> <img src="https://drive.google.com/uc?export=view&id=1UoKlEJNLB-Fr01X23nxXtWdyRBdrSTtT"> 
 5. When you get to the Service Account menu, enter whatever you want for the Part 1-Service Account Details then just skip the optional parts 2 and 3
 6. Click on the email of the created Service Account, then go to the keys menu -> add key -> create new key -> JSON to download a key.<img src="https://drive.google.com/uc?export=view&id=1Ak4NQBg-n93Bsls12BGMD1MU6iNSAAuF"> 
 7. Rename this file to "client_key.json" and move it into the directory of the .py files. Note, you should not have this file publicly accessible.

<!-- CONTACT -->
## Contact

Ryan Howell -  ryanhowell15@gmail.com

Project Link: [https://github.com/Ryguy924/Grading-Partition](https://github.com/Ryguy924/Grading-Partition)

<p align="right">(<a href="#top">back to top</a>)</p>
