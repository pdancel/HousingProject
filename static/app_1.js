var svgWidth = 960;
var svgHeight = 500;

var margin = { top: 20, right: 40, bottom: 60, left: 100 };

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select(".chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var chart = svg.append("g");

// Append a div to the body to create tooltips, assign it a class
d3.select(".chart")
  .append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

d3.json("/finaldata", function(err, Data) {
  if (err) throw err;

  Data.forEach(function(data) {
    // data.hair_length = +data.hair_length;
    // data.num_hits = +data.num_hits;
    data.median_home_price = +data.median_home_price;
    data.combined_salary = +data.combined_salary;
  });

  // Create scale functions
  var yLinearScale = d3.scaleLinear()
    .range([height, 0]);

  var xLinearScale = d3.scaleLinear()
    .range([0, width]);

  // Create axis functions
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Scale the domain
  xLinearScale.domain([35000, d3.max(Data, function(data) {
    return +data.combined_salary;
  })]);
  yLinearScale.domain([75000, d3.max(Data, function(data) {
    return +data.median_home_price;
  })]);

  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -60])
    .html(function(data) {
      var state = data.state;
      var affordability = +data.ratio_total;
      return (state + "<br> Affordability Index: " + affordability);
    });

  chart.call(toolTip);

  var elem = chart.append("g").selectAll("g")
    .data(Data)
    
  var elemEnter =elem.enter()
      .append("g")
      .attr("transform", function (data, index) {
        return "translate(" + xLinearScale(data.combined_salary) + " ," + yLinearScale(data.median_home_price) + ")"
      });
      elemEnter.append("circle")
        .attr("r", "10") 
        .attr("fill", "red")
        .on("click", function(data) {
        toolTip.show(data);
        })
        // onmouseout event
        .on("mouseout", function(data, index) {
        toolTip.hide(data);
        });
      elemEnter.append("text")
        .attr("dx", function(data, index){return 0;})
        .attr("dy", function(data, index){return 5;})
        .attr("text-anchor", "middle")
        .text(function(data, index){return data.state;})     
        .attr("font-size", 12)  
        .attr('fill', 'black')
        .on("click", function(data) {
        toolTip.show(data);
        })
        ;

  chart.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);
  
  chart.append("g")
    .call(leftAxis);

  chart.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 10)
      .attr("x", 0 - (height / 2)- 60)
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Median Home Price ($)");

// Append x-axis labels
  chart.append("text")
    .attr("transform", "translate(" + (width / 2 - 25) + " ," + (height + margin.top + 30) + ")")
    .attr("class", "axisText")
    .text("Median Salary ($)");
});


