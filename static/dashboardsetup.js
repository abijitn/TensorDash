$(document).ready(function() {
	// get the data from the server
	$.getJSON("/data").done(function(data) {
		console.log(data);
		// make the main dashboard tiles for each given statistic
		for (var stat in data) {
			// if the stat should be displayed as a line graph, then show current value and percent change
			if (data[stat]["graphType"] == "line") {
				var temp = data[stat]["values"]["values"];
				var currentValue = temp[temp.length - 1];
				$("#" + stat + "Val").html(
					data[stat]["prefix"] + 
					getFormattedValue(data, stat, currentValue) +
					data[stat]["suffix"]
				);
				displayPctChange(data, stat, currentValue, 1, stat + "Change");
				$("#" + stat + "Since").html(
					"since 1 " + 
					data[stat]["timescale"].substring(0, data[stat]["timescale"].length - 1) +
					" ago"
				);
			// if the stat is a bar graph, move it down by 20px in the div
			} else if (data[stat]["graphType"] == "bar") {
				$("#" + stat + "Plot").css({"margin-top": "20px"});
			}
			$("#dash-stat-" + stat).prepend(data[stat]["title"]);
			makePlot(data, stat, stat + "Plot");
		}
	});
});