# ECE 595 Final project
This is the code for our databases final project.

## File list

+ `bills/clean.sh`: Removes the directory where the xml bills files are currently extracted.
+ `bills/getzips.sh`: Downloads the zip files containing xml files that have government bill information (uses wget command)
+ `bills/unzipWorkingset.sh`: Unzips the downloaded zip files into a folder called `BILLSXML`
+ `billsIntoMongo.py`: Grabs all the XML files in the `bills/BILLSXML` folder, converts them into our database schema, and imports them into mongoDB
+ `billStuff.py`: Has all the logic to reduce the XML bill files to our mongoDB schema. This file is called by `billsIntoMong.py`
+ `deleteBillCollecItems.py`: deletes all the bills from the mongoDB `project` database and the `bills` collection
+ `fetchRepInfo.py`: Gets representative information from the Google Civic Info API and inserts it into our relational database
+ `importcsv.py`: Imports data from a .csv file and inserts it into the relational database.
+ `loginFucntions.py`: Contains functions that are used to add users, check for users, check if login info is correct, and one to initiate the database connection.
+ `mongo-bill-import.bat`: imports the bill information from `mongo-bills.json`
+ `mongo-bills.json`: Our current working set of bills.
+ `mongoBillExport.json`: Exports the bills from mongoDB to `mongo-bills.json`.
+ `mongoWrapper.py`: Has all the mongoDB functions that we use
+ `README.md`: Well, you're reading it.
+ `testbillStuff.py`: tests the loging for `billStuff.py`
+ `testdriver.py`: tests functions in `mongoWrapper.py`
+ `TestWindows.py`: The main file that contains the UI and wraps all the functionality together.
+ `uifunctions.py`: Has one function that generates an error window.
+ `us-115th1-congress-members.csv`: the working set of data for our represetatives.

## External libraries
These were all installed with `pip`.
+ PyMongo: (to connect to mongoDB)
+ PyODBC: (to connect to MS SQL)
+ TkInter: (for the user interface)

## Environment
We used python 3.7.3 dowloaded from the [python web site](https://www.python.org/downloads/). Pip was used to install all libraries. Windows was our development platform and we used the 64 bit version of Python.