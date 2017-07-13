/app.py
	-the main flask app
	-declares the various metrics to display and some info about them
/data.py
	-handles reading in from the Excel file
	-definition of the Statistic class
		-Statistic.info is a dictionary for each metric that gets
		sent to the client; contains all the information the front-
		end needs to display the data properly
/static
	/bootstrap.js, bootstrap.mis.css, bootstrap.min.js, jquery.js
		-publicly available js/css packages
	/dashboardsetup.js
		-functions to set up the main dashboard page with tiles for each
		metric
	/pagesetup.js
		-functions used throughout the site to make plots, tables, and other
		misc. features
	/mystyles.css
		-contains the css that I wrote for the site
	 
/templates
	/index.html
		-template that the rest of the site extends
	/dashboard.html
		-extends index.html; the html for the main dashboard
		homepage
	/drilldown.html
		-extends index.html; the html for the pages displayed when
		an individual tile on the dashboard is clicked