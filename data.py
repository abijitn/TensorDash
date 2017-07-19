import openpyxl

class Statistic:

	"""The Statistic object packages all of the information necessary
	to render a specific metric on the dashboard. It also handles loading
	data from an external source."""

	def __init__(
		self, 		
		workbook = None,
		sheetName = None,
		title = None,
		prefix = "",
		suffix = "",
		timescale = None,
		dps = 0,
		posColor = None,
		negColor = None,
		categories = None,
		hasTable = False,
		categoryToGraph = None,
		prevValueHeaders = None,
		isPercentage = False,
		sheetColumns = None,
		sheetRows = None,
		graphType = "line",
		sheetOrientation = "vertical",
		firstDataRow = 3,
		definitions = []
	):
		# workbook object that the metric is read from
		self.workbook = workbook
		# the sheet object that is 
		self.sheet = workbook[sheetName]
		self.sheetOrientation = sheetOrientation
		# the info dictionary contains all the data about this metric that will be sent to the client
		self.info = dict(
			# name to display on the tile/at the top of the page
			title = title,
			# prefix to display before values of this metric (i.e., $)
			prefix = prefix,
			# suffix to display after values of this metric (i.e., M)
			suffix = suffix,
			# string to indicate whether the information is by month, year, quarter, etc.
			timescale = timescale,
			# decimal points to display after each value for this metric
			dps = dps,
			# when this metric is positive or goes up, the color it should be
			posColor = posColor,
			# when this metric is negative or goes down, the color it should be
			negColor = negColor,
			# a list of the categories of data for this metric (i.e., ["New", "Churn", "Expansion", "Net New"])
			categories = categories,
			hasTable = hasTable,
			# which of the above categories, if any, should be graphed
			categoryToGraph = categoryToGraph,
			# the headers to display for the previous value tiles at the bottom of the page (i.e., "1 Month Ago etc." vs. "1 Week Ago etc.")
			prevValueHeaders = prevValueHeaders,
			# whether the metric should be displayed as a percentage
			isPercentage = isPercentage,
			# a dictionary that maps the keys "date," "value," and "category" to their associated capital column letters on the spreadsheet
			sheetColumns = sheetColumns,
			sheetRows = sheetRows,
			dates = [],
			values = [],
			quarters = [],
			qValues = [],
			years = [],
			yValues = [],
			allDates = [],
			firstDataRow = firstDataRow - 1,
			# a dictionary that maps category keys to a list of the values for the specific category
			categoryValues = dict(),
			# line, bar, etc.
			graphType = graphType,
			definitions = definitions
		)
		# set up the dictionary that will hold the category values
		self.initializeCategoryValuesDict()
		# read the metric data from the spreadsheet
		self.readSheet()

	def initializeCategoryValuesDict(self):
		if self.info["categories"] != None:
			for category in self.info["categories"]:
				self.info["categoryValues"][category[0]] = dict(
					values = [],
					qValues = [],
					yValues = [],
					allValues = []
				)

	def readSheet(self):
		# an iterable object (not totally sure how it's implemented -- I think it's a generator?) of the rows in the spreadsheet
		rows = self.sheet.rows
		# the current row
		rowIndex = 0
		if self.sheetOrientation == "vertical":
			for row in rows:
				# skip the top row, since it has headers instead of values
				if rowIndex != 0:
					date = ""
					value = ""
					category = ""
					# iterate over the cells in the row
					for cell in row:
						# assign the date, value, and category variables as appropriate
						if cell.column in self.info["sheetColumns"]["date"]:
							if cell.value != None:
								date += " " + str(cell.value)
						elif cell.column == self.info["sheetColumns"]["value"]:
							if cell.value != None:
								value = float(cell.value)
								if self.info["isPercentage"]:
									value *= 100
						elif cell.column == self.info["sheetColumns"]["category"]:
							if cell.value != None:
								category = cell.value
					# ensure that date and value were assigned (for some reason, the program will sometimes read in empty rows)
					if date != "" and value != "":
						# store the date, value, and category in the proper fields in self.info
						if date not in self.info["dates"]:
							self.info["dates"].append(date)
						if category != "":
							if category == self.info["categoryToGraph"]:
								self.info["values"].append(value)
							self.info["categoryValues"][category]["values"].append(value)
						else:
							self.info["values"].append(value)
				rowIndex += 1
		elif self.sheetOrientation == "horizontal":
			year = ""
			category = ""
			years = []
			dateColumns = set()
			qColumns = set()
			yColumns = set()
			for row in rows:
				cellIndex = 0
				for cell in row:
					if rowIndex == 0 and cellIndex > 0:
						if cell.value == None: 
							years.append(year)
						else:
							year = cell.value[0:2] + cell.value[4:]
							years.append(year)
					if rowIndex == 1 and cell.value != None:
						if "Q" in cell.value:
							self.info["quarters"].append(years[cellIndex - 1] + " " + cell.value)
							self.info["allDates"].append(years[cellIndex - 1] + " " + cell.value)
							qColumns.add(cell.column)
						elif "FY" in cell.value:
							self.info["years"].append(years[cellIndex - 1])
							self.info["allDates"].append(years[cellIndex - 1])
							yColumns.add(cell.column)
						else:
							self.info["dates"].append(years[cellIndex - 1] + " " + cell.value)
							self.info["allDates"].append(years[cellIndex - 1] + " " + cell.value)
							dateColumns.add(cell.column)
					if rowIndex >= self.info["firstDataRow"]:
						if cellIndex == 0 and cell.value != None:
							category = cell.value
						elif cell.value != None:
							value = float(cell.value)
							if self.info["isPercentage"]:
								value *= 100
							if cell.column in yColumns:
								self.info["categoryValues"][category]["yValues"].append(value)
							elif cell.column in qColumns:
								self.info["categoryValues"][category]["qValues"].append(value)
							elif cell.column in dateColumns:
								self.info["categoryValues"][category]["values"].append(value)
							self.info["categoryValues"][category]["allValues"].append(value)
					cellIndex += 1
				rowIndex += 1
				if category == self.info["categoryToGraph"]:
					self.info["values"] = self.info["categoryValues"][category]["values"]
					self.info["qValues"] = self.info["categoryValues"][category]["qValues"]
					self.info["yValues"] = self.info["categoryValues"][category]["yValues"]
















