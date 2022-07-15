var org_height = 480;
var org_width = 640;
//linear scale function
var x_image = d3.scaleLinear()
  .domain([0, org_width ])
  .range([ 0, 800]);

var margin = {top: 10, right: 50, bottom: 140, left: 150};


console.log(dim.image);
width = x_image(org_width)
height = x_image(org_height)

//create the svg dom
var svg = d3.select("#map").append("svg")
    .attr("width", "1400")
    .attr("height", "600")
    .append("g")
    .attr("transform","translate("+margin.left+","+margin.top+")")

//add image to the background
var myimage = svg.append('image')
    .attr('xlink:href', "../static/username/result/" + dim.image)
    .attr('width', width)
    .attr('height', height)
