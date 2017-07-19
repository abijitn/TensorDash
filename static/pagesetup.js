// format a value with commas if it's a whole number, or with the specified number of decimal points
function getFormattedValue(data, stat, value) {
    if (data[stat].dps == 0) {
        return value.toLocaleString();
    } else {
        return value.toFixed(data[stat].dps);
    }
}

// display the percent change of a stat, colored correctly and with the proper arrow
function displayPctChange(data, stat, currentValue, stepsBack, divID, timescale) {
    if (!timescale) {
        timescale = data[stat].timescale;
    }
    var valuesLength = 0;
    var prevValue = 0
    if (timescale == "Monthly") {
        valuesLength = data[stat].dates.length;
        prevValue = data[stat].values[valuesLength - 1 - stepsBack];
    } else if (timescale == "Quarterly") {
        valuesLength = data[stat].quarters.length;
        prevValue = data[stat].qValues[valuesLength - 1 - stepsBack];
    } else if (timescale == "Yearly") {
        valuesLength = data[stat].years.length;
        prevValue = data[stat].yValues[valuesLength - 1 - stepsBack];
    }
    var pctChange;
    if (data[stat].isPercentage) {
        pctChange = (currentValue - prevValue) / 100;
    } else {
        pctChange = (currentValue - prevValue) / Math.abs(prevValue);
    }
    if (pctChange >= 0) {
        $("#" + divID).html("&#9650; " + (pctChange * 100).toFixed(2) + "%")
        $("#" + divID).css({"color": data[stat].posColor});
    } else {
        $("#" + divID).html("&#9660;" + (pctChange * 100).toFixed(2) + "%")
        $("#" + divID).css({"color": data[stat].negColor})
    }
}

// display the bottom tiles that display previous values
function displayBottomTiles(data, stat) {
    var indices = [];
    var timescale = data[stat].timescale;
    if (timescale == "Monthly") {
        indices = [0, 3, 6, 9, 12];
    } else if (timescale == "Quarterly") {
        indices = [0, 1, 2, 3, 4];
    }
    var valuesLength = data[stat].dates.length;
    var currentValue = data[stat].values[valuesLength - 1];
    // calculate and display the respective previous values as determined by timescale
    for (i = 0; i < 5; i++) {
        $("#pv" + (i + 1)).prepend(
            "<span>" + data[stat].prevValueHeaders[i] + "</span>"
        );
        if (valuesLength - (indices[i] + 1) >= 0) {
            var value = data[stat].values[valuesLength - (indices[i] + 1)];
            $("#display-value" + (i + 1)).html(
                data[stat].prefix + 
                getFormattedValue(data, stat, value) + 
                data[stat].suffix
            );
            if (i > 0) {
                displayPctChange(data, stat, currentValue, indices[i], "display-pct" + (i + 1));
            }
        }
    }
}

// makePlot, unsurprisingly, uses plotly js to plot the given data in div plotDiv
function makePlot(data, stat, plotDiv, timescale) {
    if (!timescale) {
        timescale = data[stat].timescale;
    } 
    var graphX = [];
    var graphY = [];
    if (timescale == "Monthly") {
        graphX = data[stat].dates;
        graphY = data[stat].values;
    } else if (timescale == "Quarterly") {
        graphX = data[stat].quarters;
        graphY = data[stat].qValues;
    } else if (timescale == "Yearly") {
        graphX = data[stat].years;
        graphY = data[stat].yValues;
    }
    // will hold the data to be graphed
    var graphData = [];
    var prefix = data[stat].prefix;
    var suffix = data[stat].suffix;
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
    if (data[stat].graphType == "line") {
        var colLT = data[stat].negColor;
        var colGT = data[stat].posColor;
        var dps = data[stat].dps;
        var valuesLength = graphY.length;
        var currentValue = graphY[valuesLength - 1];
        // show the current value at the top
        $("#current-value").html(prefix + getFormattedValue(data, stat, currentValue) + suffix);
        // show the percent change at the top
        displayPctChange(data, stat, currentValue, 1, "pct-change", timescale);
        $("#timescale").html("since 1 " + timescale.substring(0, timescale.length - 2).toLowerCase() + " ago");
        // fill graphData appropriately
        graphData = [{
            x: graphX,
            y: graphY,
            mode: 'line',
            type: 'scatter',
            line: {
                width: 7,
                color: "#4f8ff7"
            }
        }];
    // if the data should be displayed as a bar graph
    } else if (data[stat].graphType == "bar") {
        // iterate over the metric's categories
        for (i = 0; i < data[stat].categories.length; i++) {
            var category = data[stat].categories[i][0]
            if (!category.includes("Starting") && !category.includes("Ending")) {

                var trace = {
                    x: [],
                    y: [],
                    type: null,
                    name: category,
                    marker: {
                        color: null
                    }
                }

                var values = [];

                if (timescale == "Monthly") {
                    trace.x = data[stat].dates;
                    values = data[stat].categoryValues[category].values;
                    trace.y = values;
                } else if (timescale == "Quarterly") {
                    trace.x = data[stat].quarters;
                    values = data[stat].categoryValues[category].qValues;
                    trace.y = values;
                } else if (timescale == "Yearly") {
                    trace.x = data[stat].years;
                    values = data[stat].categoryValues[category].yValues;
                    trace.y = values;
                }

                if (category == "Net New") {
                    trace.marker.color = "black";
                    trace.type = "line";
                } else {
                    trace.type = "bar";
                    if (category == "Land" || category == "Promoter") {
                        trace.marker.color = "#2CBF6D";
                    } else if (category == "Lost" || category == "Detractor") {
                        trace.y = values.map(x => -Math.abs(x));
                        trace.marker.color = "#E16070";
                    } else if (category == "Downgrade") {
                        trace.y = values.map(x => -Math.abs(x));
                        trace.marker.color = "#EFC663";
                    } else if (category == "Expand") {
                        trace.marker.color = "#7049A3";
                    } else if (category == "Passive") {
                        trace.marker.color = "#EFC663";
                    }
                }

                if (stat == "NPS" || stat == "NPSSegPct") {
                    trace.width = [0.3];
                    trace.text = (stat == "NPS") ? ["2.9"] : data[stat].categoryValues[category].values[0] + "%";
                    trace.textposition = "auto";
                    trace.textfont = {
                        color: "#ffffff"
                    };
                    trace.hoverinfo = "none";
                }

                // add data to graphData
                graphData.push(trace);
            }
        }
        // tell the bar graph to stack
        layout.barmode = "relative";
    }
    // if plotDiv was specified, then the graph will be on the dashboard instead of the drilldown; change the color if necessary and hide the axes
    if (plotDiv) {
        if (data[stat].graphType == "line") {
            graphData[0].line.color = "#e2edff";
            layout.xaxis.showticklabels = false;
            layout.xaxis.showgrid = false;
            layout.xaxis.showline = false;
            layout.xaxis.zeroline = false;
        } else {
            layout.legend = {
                font: {
                    size: 9
                }
            };
        }
        layout.yaxis.showgrid = false;
        layout.yaxis.showline = false;
        layout.yaxis.zeroline = false;
        layout.yaxis.showticklabels = false;
        layout.margin = {
            l: 0,
            r: 0,
            t: 0,
            b: 0,
            pad: 0
        };
        if (stat == "NPS" || stat == "NPSSegPct") {
            layout.xaxis.showticklabels = true;
            layout.xaxis.zeroline = true;
            if (stat == "NPS") {
                layout.annotations = [{
                    xref: 'x',
                    yref: 'y',
                    x: data[stat].dates[0],
                    y: -0.75,
                    showarrow: false,
                    text: "Sample Size = " + data[stat].sampleSize,
                    font: {
                        size: 12,
                        color: "rgb(0, 0, 0)"
                    }
                }]
                layout.margin = {
                    l: 0,
                    r: 0,
                    t: 40,
                    b: 40,
                    pad: 0
                };
            } else {
                layout.margin = {
                    l: 0,
                    r: 0,
                    t: 0,
                    b: 40,
                    pad: 0
                }
            }
        }
    // if plotDiv wasn't specified, then put the graph in the drilldown page
    } else if (!plotDiv) {
        plotDiv = "plot";
    }
    // make the plot
    Plotly.newPlot(plotDiv, graphData, layout, {displayModeBar: false});
}

// makes an individual row for a specific category in the breakout table on the drilldown page
function makeTableRow(data, id, stat, category, colLT, colGT) {
    var prefix = data[stat].prefix;
    var suffix = data[stat].suffix;
    var dps = data[stat].dps;
    var fontweight = "normal";
    var categoryName = category;
    if (category == "Total") {
        categoryName = "Ending " + stat;
        fontweight = "bold";
    }
    if (category.includes("Starting") || category.includes("Ending")) {
        fontweight = "bold";
    }
    $("#categories").append("<tr style='font-weight: " + fontweight + "'><td>" + categoryName + "</td></tr>");
    $("#category-data").append("<tr id='" + id + "' style='font-weight: " + fontweight + "'>");
    for (i = 0; i < data[stat].allDates.length; i++) {
        var val = data[stat].categoryValues[category].allValues[i];
        var bgcolor = "white";
        if (data[stat].allDates[i].includes("Q")) {
            bgcolor = "#f3f3f3";
        } else if (data[stat].allDates[i].split(" ").length == 1) {
            bgcolor = "#e5e5e5";
        }
        $("#" + id).append(
            "<td id='" + stat + id  + i + "'>" + prefix +
            getFormattedValue(data, stat, val) + suffix +
            "</td>"
        );
        if (parseFloat(data[stat].categoryValues[category].allValues[i]) < 0) {
            $("#" + stat + id + i).css({"color": colLT, "background-color": bgcolor});
        } else if (parseFloat(data[stat].categoryValues[category].allValues[i]) > 0) {
            $("#" + stat + id + i).css({"color": colGT, "background-color": bgcolor});
        }
    }
    $("#category-data").append("</tr>");
}

// makes the breakout table for the drilldown page
function makeTable(data, stat) {
    var prefix = data[stat].prefix;
    var suffix = data[stat].suffix;
    var dps = data[stat].dps;
    $("#category-data").append("<tr id='headers'>");
    for (i = 0; i < data[stat].allDates.length; i++) {
        var bgcolor = "white";
        if (data[stat].allDates[i].includes("Q")) {
            bgcolor = "#f3f3f3";
        } else if (data[stat].allDates[i].split(" ").length == 1) {
            bgcolor = "#e5e5e5";
        }
        $("#headers").append("<th style='background-color: " + bgcolor + ";'>" + data[stat].allDates[i] + "</th>");
    }
    $("#category-data").append("</tr>");
    for (category = 0; category < data[stat].categories.length; category++) {
        var id = ""
        if (data[stat].categories[category][0].includes(" ")) {
            id = data[stat].categories[category][0].replace(" ", "-");
        } else {
            id = data[stat].categories[category][0];
        }
        makeTableRow(
            data, 
            id, 
            stat, 
            data[stat].categories[category][0], 
            data[stat].categories[category][2], 
            data[stat].categories[category][1]
        );
    }
    $("#scroll").css({"height": $("#category-data").css("height")});
}


