// format a value with commas if it's a whole number, or with the specified number of decimal points
function getFormattedValue(data, stat, value) {
    if (data[stat]["dps"] == 0) {
        return value.toLocaleString();
    } else {
        return value.toFixed(data[stat]["dps"]);
    }
}

// display the percent change of a stat, colored correctly and with the proper arrow
function displayPctChange(data, stat, currentValue, stepsBack, divID) {
    var valuesLength = data[stat]["values"]["dates"].length;
    var prevValue = data[stat]["values"]["values"][valuesLength - 1 - stepsBack];
    var pctChange = (currentValue - prevValue) / Math.abs(prevValue);
    if (pctChange >= 0) {
        $("#" + divID).html("&#9650; " + (pctChange * 100).toFixed(2) + "%")
        $("#" + divID).css({"color": data[stat]["posColor"]});
    } else {
        $("#" + divID).html("&#9660;" + (pctChange * 100).toFixed(2) + "%")
        $("#" + divID).css({"color": data[stat]["negColor"]})
    }
}

// display the bottom tiles that display previous values
function displayBottomTiles(data, stat) {
    var indices = [];
    var timescale = data[stat]["timescale"];
    if (timescale == "months") {
        indices = [0, 1, 3, 6, 12];
    } else if (timescale == "quarters" || timescale == "weeks") {
        indices = [0, 1, 2, 3, 4];
    }
    var valuesLength = data[stat]["values"]["dates"].length;
    var currentValue = data[stat]["values"]["values"][valuesLength - 1];
    // calculate and display the respective previous values as determined by timescale
    for (i = 0; i < 5; i++) {
        $("#pv" + (i + 1)).prepend(
            "<span>" + data[stat]["prevValueHeaders"][i] + "</span>"
        );
        if (valuesLength - (indices[i] + 1) >= 0) {
            var value = data[stat]["values"]["values"][valuesLength - (indices[i] + 1)];
            $("#pvv" + (i + 1)).html(
                data[stat]["prefix"] + 
                getFormattedValue(data, stat, value) + 
                data[stat]["suffix"]
            );
            if (i > 0) {
                displayPctChange(data, stat, currentValue, indices[i], "pvp" + (i + 1));
            }
        }
    }
}

// makePlot, unsurprisingly, uses plotly js to plot the given data in div plotDiv
function makePlot(data, stat, plotDiv) {
    // will hold the data to be graphed
    var graphData = [];
    var prefix = data[stat]["prefix"];
    var suffix = data[stat]["suffix"];
    // specifies the layout/styling of the graph
    var layout = {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: {
            tickprefix: prefix,
            ticksuffix: suffix
        },
        xaxis: {}
    };
    // if the data should be displayed as a line graph
    if (data[stat]["graphType"] == "line") {
        var colLT = data[stat]["negColor"];
        var colGT = data[stat]["posColor"];
        var dps = data[stat]["dps"];
        var timescale = data[stat]["timescale"];
        var valuesLength = data[stat]["values"]["values"].length;
        var currentValue = data[stat]["values"]["values"][valuesLength - 1];
        // show the current value at the top
        $("#current-value").html(prefix + getFormattedValue(data, stat, currentValue) + suffix);
        // show the percent change at the top
        displayPctChange(data, stat, currentValue, 1, "pct-change", "green", "red");
        // fill graphData appropriately
        graphData = [{
            x: data[stat]["values"]["dates"],
            y: data[stat]["values"]["values"],
            mode: 'line',
            type: 'scatter',
            line: {
                width: 7,
                color: "#4f8ff7"
            }
        }];
    // if the data should be displayed as a bar graph
    } else if (data[stat]["graphType"] == "bar") {
        // iterate over the metric's categories
        for (var category in data[stat]["categoryValues"]) {
            var dates = []
            var values = []
            // increment counter by 3 each time, so graph is by quarters instead of months
            for (i = 0; i < data[stat]["categoryValues"][category]["dates"].length; i += 3) {
                if (i < data[stat]["categoryValues"][category]["dates"].length) {
                    dates.push(data[stat]["categoryValues"][category]["dates"][i]);
                    values.push(data[stat]["categoryValues"][category]["values"][i]);
                }
            }
            var trace = {
                x: dates,
                y: values,
                type: "bar",
                name: category
            }
            // add data to graphData
            graphData.push(trace);
        }
        // tell the bar graph to stack
        layout["barmode"] = "relative";
    }
    // if plotDiv was specified, then the graph will be on the dashboard instead of the drilldown; change the color if necessary and hide the axes
    if (plotDiv) {
        if (data[stat]["graphType"] == "line") {
            graphData[0]["line"]["color"] = "#e2edff";
        }
        layout["xaxis"]["showgrid"] = false;
        layout["xaxis"]["showline"] = false;
        layout["xaxis"]["zeroline"] = false;
        layout["xaxis"]["showticklabels"] = false;
        layout["yaxis"]["showgrid"] = false;
        layout["yaxis"]["showline"] = false;
        layout["yaxis"]["zeroline"] = false;
        layout["yaxis"]["showticklabels"] = false;
        layout["margin"] = {
            l: 0,
            r: 0,
            t: 0,
            b: 0,
            pad: 0
        };
    // if plotDiv wasn't specified, then put the graph in the drilldown page
    } else if (!plotDiv) {
        plotDiv = "plot";
    }
    // make the plot
    Plotly.newPlot(plotDiv, graphData, layout, {displayModeBar: false});
}

// makes an individual row for a specific category in the breakout table on the drilldown page
function makeTableRow(data, id, stat, category, colLT, colGT) {
    var prefix = data[stat]["prefix"];
    var suffix = data[stat]["suffix"];
    var dps = data[stat]["dps"];
    $("#category-data").append("<tr id='" + id + "'>");
    for (i = 0; i < data[stat]["categoryValues"][category]["dates"].length; i++) {
        var val = data[stat]["categoryValues"][category]["values"][i];
        $("#" + id).append(
            "<td id='" + stat + id  + i + "'>" + prefix +
            getFormattedValue(data, stat, val) + suffix+
            "</td>"
        );
        if (parseFloat(data[stat]["categoryValues"][category]["values"][i]) < 0) {
            $("#" + stat + id + i).css({"color": colLT});
        } else if (parseFloat(data[stat]["categoryValues"][category]["values"][i]) > 0) {
            $("#" + stat + id + i).css({"color": colGT});
        }
    }
    $("#category-data").append("</tr>");
}

// makes the breakout table for the drilldown page
function makeTable(data, stat) {
    prefix = data[stat]["prefix"]
    suffix = data[stat]["suffix"]
    dps = data[stat]["dps"]
    $("#category-data").append("<tr id='headers'>");
    for (i = 0; i < data[stat]["categoryValues"]["Net New"]["dates"].length; i++) {
        dateList = data[stat]["categoryValues"]["Net New"]["dates"][i].split(" ");
        $("#headers").append(
            "<th>" +
            dateList[2] + " " + dateList[1].substring(2, dateList[1].length) +
            "</th>"
        );
    }
    $("#category-data").append("</tr>");
    makeTableRow(data, "new", stat, "New", "red", "green");
    makeTableRow(data, "expansion", stat, "Expansion", "red", "green");
    makeTableRow(data, "churn", stat, "Churn", "green", "red");
    makeTableRow(data, "net-new", stat, "Net New", "red", "green");
}