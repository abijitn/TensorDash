function toggleOn(selector, displayStyle) {
    $(selector).css({"display": displayStyle});
}

function toggleOff(selector) {
    $(selector).css({"display": "none"});
}

function find(categories, name) {
    return categories.find(x => x.name == name);
}

function getFormattedValue(category, value) {
    if (category.dps == 0) {
        value = value.toLocaleString();
        return value.split(".")[0];
    } else {
        return value.toFixed(category.dps);
    }
}

function getCategoryValuesByTimescale(category, timescale) {
    if (timescale == "monthly") {
        return category.mValues;
    } else if (timescale == "quarterly") {
        return category.qValues;
    } else if (timescale == "yearly") {
        return category.yValues;
    }
}

function getValue(category, timescale, stepsBack) {
    var values = getCategoryValuesByTimescale(category, timescale);
    if (stepsBack >= values.length) {
        return null;
    } else {
        return values[values.length - 1 - stepsBack];
    }
}

function displayPctChange(category, stepsBack, divID, timescale) {
    var pctChange;
    var currentValue = getValue(category, timescale, 0);
    var prevValue = getValue(category, timescale, stepsBack);
    if (currentValue == null || prevValue == null) {
        return;
    }
    if (category.isPercentage) {
        pctChange = (currentValue - prevValue) / 100;
    } else {
        pctChange = (currentValue - prevValue) / Math.abs(prevValue);
    }
    if (pctChange >= 0) {
        $("#" + divID).html("&#9650; " + (pctChange * 100).toFixed(1) + "%")
        $("#" + divID).css({"color": category.posColor});
    } else {
        $("#" + divID).html("&#9660;" + (pctChange * 100).toFixed(1) + "%")
        $("#" + divID).css({"color": category.negColor})
    }
}

function displayBottomTiles(data, metric) {
    var indices = [];
    var timescale = data[metric].defaultTimescale;
    var category = find(data[metric].categories, data[metric].mainCategory);
    if (timescale == "monthly") {
        indices = [0, 3, 6, 9, 12];
    } else if (timescale == "quarterly") {
        indices = [0, 1, 2, 3, 4];
    }
    for (i = 0; i < 5; i++) {
        $("#pv" + i).prepend(
            "<span>" + data[metric].tileHeaders[i] + "</span>"
        );
        var value = getValue(category, timescale, indices[i]);
        if (value != null) {
            $("#display-value" + i).html(
                category.prefix + 
                getFormattedValue(category, value) + 
                category.suffix
            ); 
            if (i > 0) {
                displayPctChange(category, indices[i], "display-pct" + i, timescale);
            }
        }
    }
}

function makeTraces(data, metric, timescale, destination) {
    var traces = [];
    for (i = 0; i < data[metric].categories.length; i++) {
        var category = data[metric].categories[i];
        var xs = [];
        var ys = [];
        if (timescale == "monthly") {
            xs = data[metric].months;
            ys = category.mValues;
        } else if (timescale == "quarterly") {
            xs = data[metric].quarters;
            ys = category.qValues;
        } else if (timescale == "yearly") {
            xs = data[metric].years;
            ys = category.yValues;
        }
        var color;
        var visible;
        if (destination == "dashboard") {
            color = category.mainDashGraphColor;
            visible = category.onMainDashboard;
        } else if (destination == "drilldown") {
            color = category.drilldownGraphColor;
            visible = category.state;
        }
        var trace = {
            x: xs,
            y: ys,
            name: category.name,
            type: category.graphType,
            hoverinfo: "text",
            hovertext: ys.map(y => category.prefix + getFormattedValue(category, y) + category.suffix),
            line: {
                width: 7,
                color: color
            },
            marker: {
                color: color
            },
            visible: visible
        };
        if (category.yaxis > 1) {
            trace.yaxis = "y" + category.yaxis;
        }
        if (data[metric].hasGraphText) {
            trace.text = ys.map(x => category.prefix + x + category.suffix);
            trace.textposition = "auto";  
            trace.textfont = {
                color: "white"
            };
        }
        traces.push(trace);
    }
    return traces;
}

function makeDashboardPlot(data, metric, plotDiv) {
    var timescale = data[metric].defaultTimescale;
    var layout = {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: {
            showticklabels: data[metric].hasXLabelsOnMainDashboard,
            showgrid: false,
            showline: false,
            zeroline: false
        },
        legend: {
            font: {
                size: 9
            }
        },
        margin: {
            l: 0,
            r: 0,
            t: 0,
            b: 0,
            pad: 0
        },
        barmode: "relative"
    }
    if (data[metric].hasXLabelsOnMainDashboard) {
        layout.margin.b = 20;
    }
    for (yaxis = 0; yaxis < data[metric].yPrefixes.length; yaxis++) {
        var y = (yaxis == 0) ? "yaxis" : "yaxis" + (yaxis + 1);
        layout[y] = {
            showticklabels: false,
            showgrid: false,
            showline: false,
            zeroline: false
        }
    }
    var traces = makeTraces(data, metric, timescale, "dashboard");
    // make the plot
    Plotly.newPlot(plotDiv, traces, layout, {displayModeBar: false});
}

function makeDrilldownPlot(data, metric, timescale) {
    var layout = {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        barmode: "relative",
        legend: {
            x: 1.04
        }
    };
    for (yaxis = 0; yaxis < data[metric].yPrefixes.length; yaxis++) {
        if (yaxis == 0) {
            layout["yaxis"] = {
                tickprefix: data[metric].yPrefixes[yaxis],
                ticksuffix: data[metric].ySuffixes[yaxis]
            };
        } else {
            layout["yaxis" + (yaxis + 1)] = {
                tickprefix: data[metric].yPrefixes[yaxis],
                ticksuffix: data[metric].ySuffixes[yaxis],
                overlaying: "y",
                side: "right",
            };
        }
    }
    var traces = makeTraces(data, metric, timescale, "drilldown");
    Plotly.newPlot("plot", traces, layout, {displayModeBar: false});
}

function toggleTrace(data, metric, category) {
    var traceIndex = data[metric].categories.indexOf(category);
    category.state = !category.state;
    Plotly.restyle("plot", {"visible": category.state}, traceIndex);
}

function makeTableRow(data, metric, category, id) {
    var fontweight = "normal";
    if (category.name.includes("Starting") || category.name.includes("Ending")) {
        fontweight = "bold";
    }
    $("#categories").append("<tr style='font-weight: " + fontweight + "'><td>" + category.name + "</td></tr>");
    $("#category-data").append("<tr id='" + id + "' style='font-weight: " + fontweight + "'>");
    for (w = 0; w < data[metric].allDates.length; w++) {
        var val = parseFloat(category.allValues[w]);
        var bgcolor = "white";
        if (data[metric].allDates[w].includes("Q")) {
            bgcolor = "#f3f3f3";
        } else if (data[metric].allDates[w].split(" ").length == 1) {
            bgcolor = "#e5e5e5";
        }
        $("#" + id).append(
            "<td id='" + metric + id  + w + "'>" + category.prefix +
            getFormattedValue(category, val) + category.suffix +
            "</td>"
        );
        var posColor = category.posColor;
        var negColor = category.negColor;
        if (category.name.includes("Starting") || category.name.includes("Ending")) {
            var posColor = "black";
            var negColor = "black";
        }
        if (val < 0) {
            $("#" + metric + id + w).css({"color": negColor, "background-color": bgcolor});
        } else if (val >= 0) {
            $("#" + metric + id + w).css({"color": posColor, "background-color": bgcolor});
        }
    }
    $("#category-data").append("</tr>");
}

function makeTable(data, metric) {
    $("#category-data").append("<tr id='headers'>");
    for (i = 0; i < data[metric].allDates.length; i++) {
        var bgcolor = "white";
        if (data[metric].allDates[i].includes("Q")) {
            bgcolor = "#f3f3f3";
        } else if (data[metric].allDates[i].split(" ").length == 1) {
            bgcolor = "#e5e5e5";
        }
        $("#headers").append("<th style='background-color: " + bgcolor + ";'>" + data[metric].allDates[i] + "</th>");
    }
    $("#category-data").append("</tr>");
    var length = data[metric].categories.length;
    $(".breakout-table").css({"height": (length + 1) * 40 + "px"});
    for (j = 0; j < length; j++) {
        var category = data[metric].categories[j];
        var id = category.name.split(" ").join("-").replace(":", "");
        makeTableRow(data, metric, category, id);
    }
    $("#scroll").css({"height": $("#category-data").css("height")});
}

