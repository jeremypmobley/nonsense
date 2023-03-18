
# jeremyruns.com

Code related to the creation and update of jeremyruns.com, a personal s3 static website to track my daily running progress

Code included here:
* update_jeremyruns.py  
Python script to update files used in hosting jeremyruns.com

* run_log_charts.ipynb  
Development notebook to create and update index.html file and charts

* jeremyruns_architecture.html  
An html doc showing the architecture involved in supporting jeremyruns.com

* index.html
* favicon.png


## Next steps:
* Clean up repo
  * Only include files listed
  * Create /dev folder
  * Add html files to repo
* Clean up code
  * Move step to move data from google sheets to s3 to separate file
  * Move step to move chart to s3 to separate function
  * Move functions to create charts to separate utils file
* Charts
  * Weekly chart - update xlabels to be date to start week
* Add text of metrics between charts in html
* Add calendar daily box heat map
  * https://pythonhosted.org/calmap/



### AWS Lambda
#### pip install pandas matplotlib fsspec tox tox-conda gspread gspread_dataframe


