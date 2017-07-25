import openpyxl

class Color:

	LIGHTGREEN = "#2cbf6d"
	PURPLE = "#7049a3"
	ORANGE = "#efc663"
	LIGHTRED = "#E16070"
	BLACK = "black"
	RED = "red"
	GREEN = "green"
	DARKBLUE = "#1890fc"
	LIGHTBLUE = "#e2edff"
	AQUA = "#82e5d2"

class State:

	ON = True
	OFF = False

class Category:

	def Default():
		return dict(
			name = "Default",
			prefix = "",
			suffix = "",
			posColor = Color.GREEN,
			negColor = Color.RED,
			isPercentage = False,
			negate = False,
			dps = 0,
			onMainDashboard = True,
			isValueOnMainDashboard = True,
			isValueOnDrilldown = True,
			state = State.ON,
			graphType = "line",
			mainDashGraphColor = Color.DARKBLUE,
			drilldownGraphColor = Color.DARKBLUE,
			yaxis = 1
		)


	def Starting(metricName, prefix = "", suffix = "", dps = 0, state = State.OFF, graphType = "line", 
		definition = dict(text = "Lorem Ipsum", color = Color.BLACK)):
		return dict(
            name = "Starting " + metricName,
            prefix = prefix,
            suffix = suffix,
            posColor = Color.GREEN,
            negColor = Color.RED,
            isPercentage = False,
            negate = False,
            dps = dps,
            onMainDashboard = False,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = state,
            graphType = state,
            drilldownGraphColor = Color.AQUA,
            definition = definition,
            yaxis = 1
        )

	def New(prefix = "", suffix = "", dps = 0, onMainDashboard = False, state = State.OFF, graphType = "line",
		definition = dict(text = "Lorem Ipsum", color = Color.LIGHTGREEN)):
		return dict(
            name = "New",
            prefix = prefix,
            suffix = suffix,
            posColor = Color.GREEN,
            negColor = Color.GREEN,
            isPercentage = False,
            negate = False,
            dps = dps,
            onMainDashboard = onMainDashboard,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = state,
            graphType = graphType,
            drilldownGraphColor = Color.LIGHTGREEN,
            mainDashGraphColor = Color.LIGHTGREEN,
            definition = definition,
            yaxis = 1
        )

	def Expand(prefix = "", suffix = "", dps = 0, onMainDashboard = False, state = State.OFF, graphType = "line",
		definition = dict(text = "Lorem Ipsum", color = Color.LIGHTGREEN)):
		return dict(
            name = "Expand",
            prefix = prefix,
            suffix = suffix,
            posColor = Color.GREEN,
            negColor = Color.GREEN,
            isPercentage = False,
            negate = False,
            dps = dps,
            onMainDashboard = onMainDashboard,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = state,
            graphType = graphType,
            drilldownGraphColor = Color.PURPLE,
            mainDashGraphColor = Color.PURPLE,
            definition = definition,
            yaxis = 1
        )

	def Downgrade(prefix = "", suffix = "", dps = 0, onMainDashboard = False, state = State.OFF, graphType = "line", 
		definition = dict(text = "Lorem Ipsum", color = Color.LIGHTRED)):
		return dict(
            name = "Downgrade",
            prefix = prefix,
            suffix = suffix,
            posColor = Color.RED,
            negColor = Color.RED,
            isPercentage = False,
            negate = True,
            dps = dps,
            onMainDashboard = onMainDashboard,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = state,
            graphType = graphType,
            drilldownGraphColor = Color.ORANGE,
            mainDashGraphColor = Color.ORANGE,
            definition = definition,
            yaxis = 1
        )

	def Churned(prefix = "", suffix = "", dps = 0, onMainDashboard = False, state = State.OFF, graphType = "line",
		definition = dict(text = "Lorem Ipsum", color = Color.LIGHTRED)):
		return dict(
            name = "Churned",
            prefix = prefix,
            suffix = suffix,
            posColor = Color.RED,
            negColor = Color.RED,
            isPercentage = False,
            negate = True,
            dps = dps,
            onMainDashboard = onMainDashboard,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = state,
            graphType = graphType,
            drilldownGraphColor = Color.LIGHTRED,
            mainDashGraphColor = Color.LIGHTRED,
            definition = definition,
            yaxis = 1
        )

	def NetNew(prefix = "", suffix = "", dps = 0, onMainDashboard = False, state = State.OFF, graphType = "line",
		definition = dict(text = "Lorem Ipsum", color = Color.LIGHTGREEN)):
		return dict(
			name = "Net New",
            prefix = prefix,
            suffix = suffix,
            posColor = Color.GREEN,
            negColor = Color.RED,
            isPercentage = False,
            negate = False,
            dps = dps,
            onMainDashboard = onMainDashboard,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = state,
            graphType = graphType,
            drilldownGraphColor = Color.BLACK,
            mainDashGraphColor = Color.BLACK,
            definition = definition,
            yaxis = 1
		)

	def Ending(metricName, prefix = "", suffix = "", dps = 0, onMainDashboard = True, state = State.ON, graphType = "line",
		definition = dict(text = "Lorem Ipsum", color = Color.BLACK)):
		return dict(
            name = "Ending " + metricName,
            prefix = prefix,
            suffix = suffix,
            posColor = Color.GREEN,
            negColor = Color.RED,
            isPercentage = False,
            negate = False,
            dps = dps,
            onMainDashboard = onMainDashboard,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = True,
            state = state,
            graphType = graphType,
            drilldownGraphColor = Color.DARKBLUE,
            mainDashGraphColor = Color.DARKBLUE,
            definition = definition,
            yaxis = 1
        )

class CategoryList:

	def __init__(self, categories):
		self.categories = categories

	def findCategory(self, categoryName):
		try:
			return list(filter(lambda x: x["name"] == categoryName, self.categories))[0]
		except:
			return None

class Metric:

	def __init__(
		self,
		workbook = None,
		sheetName = None,
		title = None,
		defaultTimescale = None,
		mainCategory = "Default",
		yPrefixes = [""],
		ySuffixes = [""],
		hasSplitTileOnMainDashboard = False,
		splitTileOtherMetric = None,
		hasTable = False,
		hasTimeOptions = True,
		hasCategoryFilters = False,
		hasDefinitions = False,
		hasCurrentValue = True,
		hasBottomTiles = True,
		hasGraphText = False,
		hasXLabelsOnMainDashboard = False,
		tileHeaders = [],
		sheetOrientation = "horizontal",
		sheetColumns = dict(),
		categories = None,
		firstDataRow = 3
	):
		self.workbook = workbook
		self.sheet = workbook[sheetName]
		self.sheetOrientation = sheetOrientation
		self.firstDataRow = firstDataRow - 1
		self.sheetColumns = sheetColumns
		self.info = dict(
			title = title,
			defaultTimescale = defaultTimescale,
			mainCategory = mainCategory,
			yPrefixes = yPrefixes,
			ySuffixes = ySuffixes,
			hasSplitTileOnMainDashboard = hasSplitTileOnMainDashboard,
			splitTileOtherMetric = splitTileOtherMetric,
			hasGraphText = hasGraphText,
			hasXLabelsOnMainDashboard = hasXLabelsOnMainDashboard,
			hasTable = hasTable,
			hasBottomTiles = hasBottomTiles,
			hasTimeOptions = hasTimeOptions,
			hasCategoryFilters = hasCategoryFilters,
			hasDefinitions = hasDefinitions,
			hasCurrentValue = hasCurrentValue,
			tileHeaders = tileHeaders,
			months = [],
			quarters = [],
			years = [],
			allDates = [],
			categories = categories
		)
		if (categories == None):
			self.info["categories"] = CategoryList([Category.Default()]);
		self.initializeCategoryValuesDict()
		self.readSheet()
		self.info["categories"] = self.info["categories"].categories

	def initializeCategoryValuesDict(self):
		for i in range(len(self.info["categories"].categories)):
			self.info["categories"].categories[i]["mValues"] = []
			self.info["categories"].categories[i]["qValues"] = []
			self.info["categories"].categories[i]["yValues"] = []
			self.info["categories"].categories[i]["allValues"] = []

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
					# iterate over the cells in the row
					for cell in row:
						# assign the date, value, and category variables as appropriate
						if cell.column in self.sheetColumns["date"]:
							if cell.value != None:
								date += " " + str(cell.value)
						elif cell.column == self.sheetColumns["value"]:
							if cell.value != None:
								value = float(cell.value)
					# ensure that date and value were assigned (for some reason, the program will sometimes read in empty rows)
					if date != "" and value != "":
						# store the date, value, and category in the proper fields in self.info
						self.info["months"].append(date)
						self.info["categories"].findCategory("Default")["mValues"].append(value)
				rowIndex += 1
		elif self.sheetOrientation == "horizontal":
			year = ""
			category = ""
			years = []
			mColumns = set()
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
							self.info["months"].append(years[cellIndex - 1] + " " + cell.value)
							self.info["allDates"].append(years[cellIndex - 1] + " " + cell.value)
							mColumns.add(cell.column)
					if rowIndex >= self.firstDataRow:
						if cellIndex == 0 and cell.value != None:
							category = self.info["categories"].findCategory(cell.value)
						elif cell.value != None and category != None:
							value = float(cell.value)
							if category["isPercentage"]:
								value *= 100
							if category["negate"]:
								value *= -1
							if cell.column in yColumns:
								category["yValues"].append(value)
							elif cell.column in qColumns:
								category["qValues"].append(value)
							elif cell.column in mColumns:
								category["mValues"].append(value)
							category["allValues"].append(value)
					cellIndex += 1
				rowIndex += 1

# the dictionary that will be sent to the webpage
data = dict()

prevValuesByMonth = [
    "Current",
    "3 Months Ago",
    "6 Months Ago",
    "9 Months Ago",
    "1 Year Ago"
]

prevValuesByQuarter = [
    "Current",
    "1 Quarter Ago",
    "2 Quarters Ago",
    "3 Quarters Ago",
    "1 Fiscal Year Ago"
]

# open the excel file
wb = openpyxl.load_workbook("AgileCentralData.xlsx")

data["ARR"] = Metric(
    workbook = wb,
    sheetName = "ARR",
    title = "Annual Recurring Revenue (ARR)",
    defaultTimescale = "monthly",
    mainCategory = "Ending ARR",
    yPrefixes = ["$"],
    ySuffixes = ["M"],
    hasTable = True,
    hasCategoryFilters = True,
    hasDefinitions = True,
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        Category.Starting("ARR", prefix = "$", suffix = "M", dps = 1),
        Category.New(prefix = "$", suffix = "M", dps = 1),
        Category.Expand(prefix = "$", suffix = "M", dps = 1),
        Category.Downgrade(prefix = "$", suffix = "M", dps = 1),
        Category.Churned(prefix = "$", suffix = "M", dps = 1),
        Category.NetNew(prefix = "$", suffix = "M", dps = 1),
        Category.Ending("ARR", prefix = "$", suffix = "M", dps = 1)
    ])
).info

data["ARRDetailed"] = Metric(
    workbook = wb,
    sheetName = "ARR",
    title = "ARR Detailed",
    defaultTimescale = "quarterly",
    mainCategory = None,
    yPrefixes = ["$"],
    ySuffixes = ["M"],
    hasTable = False,
    hasCategoryFilters = False,
    hasDefinitions = True,
    hasBottomTiles = False,
    categories = CategoryList([
        Category.New(prefix = "$", suffix = "M", dps = 1, graphType = "bar", onMainDashboard = True, state = State.ON),
        Category.Expand(prefix = "$", suffix = "M", dps = 1, graphType = "bar", onMainDashboard = True, state = State.ON),
        Category.Downgrade(prefix = "$", suffix = "M", dps = 1, graphType = "bar", onMainDashboard = True, state = State.ON),
        Category.Churned(prefix = "$", suffix = "M", dps = 1, graphType = "bar", onMainDashboard = True,
                        state = State.ON),
        Category.NetNew(prefix = "$", suffix = "M", dps = 1, onMainDashboard = True, state = State.ON)
    ])
).info

data["LTV"] = Metric(
    workbook = wb,
    sheetName = "LTV",
    title = "Lifetime Value (LTV)",
    defaultTimescale = "monthly",
    mainCategory = "LTV",
    yPrefixes = ["$"],
    ySuffixes = ["K"],
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        dict(
            name = "LTV",
            prefix = "$",
            suffix = "K",
            posColor = Color.GREEN,
            negColor = Color.RED,
            isPercentage = False,
            dps = 0,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = True,
            state = State.ON,
            graphType = "line",
            mainDashGraphColor = Color.DARKBLUE,
            drilldownGraphColor = Color.DARKBLUE,
            yaxis = "y1"
        )
    ])
).info

data["CAC"] = Metric(
    workbook = wb,
    sheetName = "CAC",
    title = "Customer Acquisition Cost (CAC)",
    defaultTimescale = "monthly",
    mainCategory = "CAC",
    yPrefixes = ["$"],
    ySuffixes = ["K"],
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        dict(
            name = "CAC",
            prefix = "$",
            suffix = "K",
            posColor = Color.RED,
            negColor = Color.GREEN,
            isPercentage = False,
            dps = 0,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = True,
            state = State.ON,
            graphType = "line",
            mainDashGraphColor = Color.DARKBLUE,
            drilldownGraphColor = Color.DARKBLUE,
            yaxis = "y1"
        )
    ])
).info

data["LTV-CACRatio"] = Metric(
    workbook = wb,
    sheetName = "LTVCAC",
    title = "LTV-CAC Ratio",
    defaultTimescale = "monthly",
    mainCategory = "LTV-CAC Ratio",
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        dict(
            name = "LTV-CAC Ratio",
            prefix = "",
            suffix = "",
            posColor = Color.GREEN,
            negColor = Color.RED,
            isPercentage = False,
            dps = 1,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = True,
            state = State.ON,
            graphType = "line",
            mainDashGraphColor = Color.DARKBLUE,
            drilldownGraphColor = Color.DARKBLUE,
            yaxis = "y1"
        )
    ])
).info

data["Customers"] = Metric(
    workbook = wb,
    sheetName = "Customers",
    title = "Customers",
    defaultTimescale = "monthly",
    mainCategory = "Ending Customers",
    hasTable = True,
    hasCategoryFilters = True,
    hasDefinitions = True,
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        Category.Starting("Customers"),
        Category.New(),
        Category.Expand(),
        Category.Downgrade(),
        Category.Churned(),
        Category.NetNew(),
        Category.Ending("Customers")
    ])
).info

data["Seats"] = Metric(
    workbook = wb,
    sheetName = "Seats",
    title = "Seats",
    defaultTimescale = "monthly",
    mainCategory = "Ending Seats",
    hasTable = True,
    hasCategoryFilters = True,
    hasDefinitions = True,
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        Category.Starting("Seats"),
        Category.New(),
        Category.Expand(),
        Category.Downgrade(),
        Category.Churned(),
        Category.NetNew(),
        Category.Ending("Seats")
    ])
).info

data["ARRChurnPct"] = Metric(
    workbook = wb,
    sheetName = "ARRChurnPct",
    title = "ARR Churn Rate",
    defaultTimescale = "monthly",
    mainCategory = "ARR Churn Rate",
    ySuffixes = ["%"],
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        dict(
            name = "ARR Churn Rate",
            prefix = "",
            suffix = "%",
            posColor = Color.RED,
            negColor = Color.GREEN,
            isPercentage = True,
            dps = 1,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = True,
            state = State.ON,
            graphType = "line",
            drilldownGraphColor = Color.DARKBLUE,
            mainDashGraphColor = Color.DARKBLUE,
            definition = "",
            yaxis = "y1"
        )
    ])
).info

data["SeatChurnPct"] = Metric(
    workbook = wb,
    sheetName = "SeatChurnPct",
    title = "Seats Churn Rate",
    defaultTimescale = "monthly",
    mainCategory = "Seats Churn Rate",
    ySuffixes = ["%"],
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        dict(
            name = "Seats Churn Rate",
            prefix = "",
            suffix = "%",
            posColor = Color.RED,
            negColor = Color.GREEN,
            isPercentage = True,
            dps = 1,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = True,
            state = State.ON,
            graphType = "line",
            drilldownGraphColor = Color.DARKBLUE,
            mainDashGraphColor = Color.DARKBLUE,
            definition = "",
            yaxis = "y1"
        )
    ])
).info

data["ARPA"] = Metric(
    workbook = wb,
    sheetName = "ARPA",
    title = "Avg. Revenue Per Account (ARPA)",
    defaultTimescale = "monthly",
    mainCategory = "Ending ARPA",
    yPrefixes = ["$"],
    ySuffixes = ["K"],
    hasTable = True,
    hasCategoryFilters = True,
    hasDefinitions = True,
    tileHeaders = prevValuesByMonth,
    categories = CategoryList([
        Category.Starting("ARPA", prefix = "$", suffix = "K", dps = 0),
        Category.New(prefix = "$", suffix = "K", dps = 0),
        Category.Expand(prefix = "$", suffix = "K", dps = 0),
        Category.Downgrade(prefix = "$", suffix = "K", dps = 0),
        Category.Churned(prefix = "$", suffix = "K", dps = 0),
        Category.NetNew(prefix = "$", suffix = "K", dps = 0),
        Category.Ending("ARPA", prefix = "$", suffix = "K", dps = 0)
    ])
).info

data["NoOfTrialsRequested"] = Metric(
    workbook = wb,
    sheetName = "NoOfTrialsRequested",
    title = "Number of Trials Requested",
    sheetOrientation = "vertical",
    defaultTimescale = "monthly",
    tileHeaders = prevValuesByMonth,
    hasTimeOptions = False,
    sheetColumns = dict(
        date = "A",
        value = "B"
    )
).info

data["SAOs"] = Metric(
    workbook = wb,
    title = "Sales Accepted Opportunities",
    sheetName = "SAOs",
    sheetOrientation = "vertical",
    defaultTimescale = "monthly",
    tileHeaders = prevValuesByMonth,
    hasTimeOptions = False,
    sheetColumns = dict(
        date = "A",
        value = "B"
    )
).info

data["SRLs"] = Metric(
    workbook = wb,
    title = "Sales Ready Leads",
    sheetName = "SRLs",
    sheetOrientation = "vertical",
    defaultTimescale = "monthly",
    tileHeaders = prevValuesByMonth,
    hasTimeOptions = False,
    sheetColumns = dict(
        date = "A",
        value = "B"
    )
).info

data["Usage"] = Metric(
    workbook = wb,
    sheetName = "Usage",
    title = "Usage",
    yPrefixes = ["", ""],
    ySuffixes = ["", "%"],
    defaultTimescale = "monthly",
    mainCategory = None,
    hasBottomTiles = False,
    hasTable = True,
    hasCategoryFilters = True,
    hasDefinitions = True,
    categories = CategoryList([
        dict(
            name = "Total Seats",
            prefix = "",
            suffix = "",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = False,
            negate = False,
            dps = 0,
            onMainDashboard = False,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.OFF,
            graphType = "line",
            drilldownGraphColor = Color.DARKBLUE,
            mainDashGraphColor = Color.DARKBLUE,
            definition = dict(text = "Lorem Ipsum", color = Color.BLACK),
            yaxis = 1
        ),
        dict(
            name = "Paid Seats",
            prefix = "",
            suffix = "",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = False,
            negate = False,
            dps = 0,
            onMainDashboard = True,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.ON,
            graphType = "line",
            drilldownGraphColor = Color.AQUA,
            mainDashGraphColor = Color.AQUA,
            definition = dict(text = "Lorem Ipsum", color = Color.BLACK),
            yaxis = 1
        ),
        dict(
            name = "Monthly Active Users",
            prefix = "",
            suffix = "",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = False,
            negate = False,
            dps = 0,
            onMainDashboard = True,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = False,
            state = State.ON,
            graphType = "line",
            drilldownGraphColor = Color.LIGHTGREEN,
            mainDashGraphColor = Color.LIGHTGREEN,
            definition = dict(text = "Lorem Ipsum", color = Color.BLACK),
            yaxis = 1
        ),
        dict(
            name = "Daily Active Users",
            prefix = "",
            suffix = "",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = False,
            negate = False,
            dps = 0,
            onMainDashboard = True,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.ON,
            graphType = "line",
            drilldownGraphColor = Color.PURPLE,
            mainDashGraphColor = Color.PURPLE,
            definition = dict(text = "Lorem Ipsum", color = Color.BLACK),
            yaxis = 1
        ),
        dict(
            name = "MAU-Paid Seats Ratio",
            prefix = "",
            suffix = "%",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = True,
            negate = False,
            dps = 1,
            onMainDashboard = False,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.OFF,
            graphType = "line",
            drilldownGraphColor = Color.ORANGE,
            mainDashGraphColor = Color.ORANGE,
            definition = dict(text = "Lorem Ipsum", color = Color.BLACK),
            yaxis = 2
        ),
        dict(
            name = "DAU-Paid Seats Ratio",
            prefix = "",
            suffix = "%",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = True,
            negate = False,
            dps = 1,
            onMainDashboard = False,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.OFF,
            graphType = "line",
            drilldownGraphColor = Color.LIGHTRED,
            mainDashGraphColor = Color.LIGHTRED,
            definition = dict(text = "Lorem Ipsum", color = Color.BLACK),
            yaxis = 2
        )
    ])
).info

data["NPS"] = Metric(
    workbook = wb,
    sheetName = "NPS",
    title = "Net Promoter Score (NPS)",
    hasTimeOptions = False,
    mainCategory = "NPS",
    defaultTimescale = "yearly",
    hasGraphText = True,
    ySuffixes = ["%"],
    hasXLabelsOnMainDashboard = True,
    hasBottomTiles = False,
    hasDefinitions = True,
    categories = CategoryList([
        dict(
            name = "NPS",
            prefix = "",
            suffix = "",
            isPercentage = False,
            dps = 1,
            negate = False,
            onMainDashboard = False,
            isValueOnMainDashboard = True,
            isValueOnDrilldown = True,
            drilldownGraphColor = Color.DARKBLUE,
            state = State.OFF,
            definition = dict(text = "Lorem Ipsum", color = Color.DARKBLUE)
        ),
        dict(
            name = "Promoter",
            prefix = "",
            suffix = "%",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = True,
            dps = 1,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.ON,
            graphType = "bar",
            drilldownGraphColor = Color.LIGHTGREEN,
            mainDashGraphColor = Color.LIGHTGREEN,
            definition = dict(text = "Lorem Ipsum", color = Color.LIGHTGREEN),
            yaxis = "y1"
        ),
        dict(
            name = "Passive",
            prefix = "",
            suffix = "%",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = True,
            dps = 1,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.ON,
            graphType = "bar",
            drilldownGraphColor = Color.ORANGE,
            mainDashGraphColor = Color.ORANGE,
            definition = dict(text = "Lorem Ipsum", color = Color.ORANGE),
            yaxis = "y1"
        ),
        dict(
            name = "Detractor",
            prefix = "",
            suffix = "%",
            posColor = Color.BLACK,
            negColor = Color.BLACK,
            isPercentage = True,
            dps = 1,
            negate = False,
            onMainDashboard = True,
            isValueOnMainDashboard = False,
            isValueOnDrilldown = False,
            state = State.ON,
            graphType = "bar",
            drilldownGraphColor = Color.LIGHTRED,
            mainDashGraphColor = Color.LIGHTRED,
            definition = dict(text = "Lorem Ipsum", color = Color.LIGHTRED),
            yaxis = "y1"
        )
    ])
).info

"""THIS LIST CONTROLS THE TILES DISPLAYED ON THE WEBSITE. THE NAMES HERE
SHOULD MATCH THE DICTIONARY KEYS AND RESPECTIVE SHEET NAMES EXACTLY. IN ORDER
TO ADD A NEW METRIC TO THE SITE, ADD THE NAME TO THE METRICS LIST AND INITIALIZE
A NEW METRIC OBJECT AS DEMONSTRATED BELOW."""
metrics = [
    "ARR",
    "ARRDetailed",
    "LTV",
    "CAC",
    "LTV-CACRatio",
    "Customers",
    "Seats",
    "ARRChurnPct",
    "ARPA",
    "SeatChurnPct",
    "Usage",
    "NoOfTrialsRequested",
    "SAOs",
    "SRLs",
    "NPS"
]
















