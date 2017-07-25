$(document).ready(function() {
	// get the data from the server
	$.getJSON("/data").done(function(data) {
		console.log(data);
		// make the main dashboard tiles for each given statistic
		for (var metric in data) {
			if (data[metric].mainCategory != null) {
				var category = data[metric].categories.find(x => x.name == data[metric].mainCategory);
				var currentValue = getValue(category, data[metric].defaultTimescale, 0);
				$("#" + metric + "Val").html(
					category.prefix + 
					getFormattedValue(category, currentValue) +
					category.suffix
				);
				var stepsBack = 3;
				if (data[metric].defaultTimescale == "quarterly") {
					stepsBack = 1;
				}
				var hasPctChange = displayPctChange(category, stepsBack, metric + "Change", data[metric].defaultTimescale);
				if (hasPctChange) {
					$("#" + metric + "Since").html("since 3 months ago");
				}
			}
			$("#dash-metric-" + metric).html(data[metric].title);
			$("#" + metric).append("<div class='dash-plot' id='" + metric + "Plot'></div>")
			makeDashboardPlot(data, metric, metric + "Plot");
		}
		$(".print-button").click(function() {
			window.print();
		});
	});
});