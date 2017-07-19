$(document).ready(function() {
	// get the data from the server
	$.getJSON("/data").done(function(data) {
		console.log(data);
		// make the main dashboard tiles for each given statistic
		for (var stat in data) {
			// if the stat should be displayed as a line graph, then show current value and percent change
			if (data[stat].graphType == "line") {
				var temp = data[stat].values;
				var currentValue = temp[temp.length - 1];
				$("#" + stat + "Val").html(
					data[stat].prefix + 
					getFormattedValue(data, stat, currentValue) +
					data[stat].suffix
				);
				var stepsBack = 0;
				var timeIntervalStr = "";
				if (data[stat].categoryToGraph) {
					stepsBack = 1;
					//timeIntervalStr = data[stat]["timescale"];
				} else {
					stepsBack = 3;
					//timeIntervalStr = data[stat]["timescale"].substring(0, data[stat]["timescale"].length - 1);
				}
				displayPctChange(data, stat, currentValue, stepsBack, stat + "Change");
				$("#" + stat + "Since").html(
					"since 3 months ago"
				);
			// if the stat is a bar graph, move it down by 20px in the div
			} else if (data[stat].graphType == "bar") {
				$("#" + stat + "Plot").css({"margin-top": "20px"});
			}
			$("#dash-stat-" + stat).prepend(data[stat].title);
			makePlot(data, stat, stat + "Plot");
		}
	});
});