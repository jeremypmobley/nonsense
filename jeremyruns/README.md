
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
* Clean up repo to only include files listed
  * Create /dev folder
  * Check in all new code from notebook, files
* Clean up code
  * Move step to move data from google sheets to s3 to separate file
  * Make index.html static, remove steps to update
  * Move functions to create charts to separate utils file
  * Move step to invalidate Cloudfront distribution to separate file
  * Move step to move chart to s3 to separate function
* Charts
  * Add space between charts so full index labels show
  * Make label rotation same across all charts
  * Daily chart - Add labels on bars
  * Daily chart - show xtick labels for each day
  * Daily chart - fix title size
  * Weekly chart - remove 2023-52 wk final data point
  * Weekly chart - update xlabels to be date to start week
* Add metrics between charts
* Add calendar daily box heat map
  * https://pythonhosted.org/calmap/
* 