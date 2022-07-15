// setting up
var exists = new Boolean(false);
var deltaX;
var org_height = 480;
var org_width = 640;
var x_image = d3.scaleLinear()
  .domain([0, org_width ])
  .range([ 0, 800]);


var margin = {top: 60, right: 50, bottom: 140, left: 150};


width = x_image(org_width);
height = x_image(org_height);

var svg = d3.select("#map").append("svg")
    .attr("width", "1400")
    .attr("height", "600")
    .append("g")
    .attr("transform","translate("+margin.left+","+margin.top+")");


// spectrum slider bar module
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;
const g1 = svg.append('g').attr('id', 'maingroup')
                           .attr('transform', `translate(${margin.left}, ${margin.top})`);
const xValue = (datum) => {return datum['X']};
const yValue = (datum) => {return datum['Y']};
let xSacle, yScale;
let alldates;
let allkeys;
let duration = 400;

// initial the canvas
const render_init = function(data){
    xScale = d3.scaleLinear()
    .domain(d3.extent(data, xValue))
    .range([0, innerWidth])
    .nice();

    yScale = d3.scaleLinear()
    .domain([d3.max(data, yValue), d3.min(data, yValue)])
    .range([0, innerHeight])
    .nice();

    // Adding axes
    const xAxis = d3.axisBottom(xScale)
    .ticks(15);
    const xAxisGroup = g1.append('g').call(xAxis)
    .attr('transform', `translate(0, ${innerHeight})`)
    .append("text")
    .text("Energy Loss[eV]")
    .attr("text-anchor","end")
    .attr("font-size","2em")
    .attr("fill", "#504f4f")
    .attr("dx","7.5em")
    .attr("dy","-0.3em");

    const yAxis = d3.axisLeft(yScale).tickSize(-innerWidth);
    const yAxisGroup = g1.append('g').call(yAxis)
                                     .append("text")
                                     .text("Intensity")
                                     .attr("transform","rotate(-90)")
                                     .attr("text-anchor","end")
                                     .attr("dy","1em")
                                     .attr("fill", "#504f4f")
                                     .attr('font-size', '2em');

    g1.selectAll('.tick text').attr('font-size', '2em');
    g1.append('path').attr('id', 'alterPath');
};
// update the spectrum chart
const render_update_alter = function(data){
      const g1 = d3.select('#maingroup');
      let time = data[0]['TimeStep'];
      time ++;
      g1.selectAll('.date_text').remove();
      g1.append("text")
        .attr('class', 'date_text')
        .attr("x", innerWidth)
        .attr("y", innerHeight / 10 - 100)
        .attr("dy", ".5em")
        .style("text-anchor", "end")
        .attr("fill", "#504f4f")
        .attr('font-size', '2em')
        .attr('font-weight', 'bold')
        .text(`Current TimeStep: ${time}`);




      const line = d3.line()
                     .x( d=> xScale(xValue(d)) )
                     .y( d=> yScale(yValue(d)) )
                     .curve( d3.curveCardinal.tension(0.5) );

      d3.select('#alterPath').datum(data)
                             .attr('stroke','orange')
                             .attr('stroke-width',2.5)
                             .attr('fill','none')
                             .transition()//.duration(duration)
                             .attr('d', line);

};

var path = './static/username/images/' + dim.csv;
console.log(path);
d3.csv(path).then(function(data){
    alldates = Array.from( new Set( data.map(d => d['TimeStep'])));

    data.forEach(d=>{

      d['X'] = +(d['X']);
      d['Y'] = +(d['Y']);
    })

    let alltimedata = {};

    allkeys = Array.from( new Set( data.map(d => d['TimeStep'])));

    allkeys.forEach( key => {
      alltimedata[key] = [];
    });

    data.forEach(d => {
      alltimedata[d['TimeStep']].push(d);
    });

    allkeys.forEach( key => {
      alltimedata[key] = alltimedata[key].sort((a,b) => {
          return b['X'] - a['X'];
      })
    })

    render_init(data);
    render_update_alter(alltimedata[allkeys[0]]);
    var slider = d3.select('#mySlider');
        slider.on('change', function() {
            let key = allkeys[this.value];
            render_update_alter(alltimedata[key]);
        });
});

//update text module
function updateTextInput(val) {
          val++;
          document.getElementById('textInput').value=val;
        }



//reset module
function reset_value()
{
    if (exists == true)
    {
        exists == false;
    }

    console.log(1);
    d3.select("#left_line").remove();
    d3.select("#right_line").remove();
}



//drag module
var dragleft = d3.drag()
    .on("start", function () {
        var current = d3.select(this);
        deltaX = current.attr("x1") - event.x;
    })
    .on("drag", function (d) {
        d3.select(this)
            .attr("x1", d.x1 =event.x + deltaX)
            .attr("x2", d.x2 = event.x + deltaX)
        document.getElementById('textInput2').value=d.x1;
    })
    ;

var dragright = d3.drag()
    .on("start", function () {
        var current = d3.select(this);
        deltaX = current.attr("x1") - event.x;
    })
    .on("drag", function (d) {
        d3.select(this)
            .attr("x1", d.x1 =event.x + deltaX)
            .attr("x2", d.x2 = event.x + deltaX)
        document.getElementById('textInput3').value=d.x1;
    });


function add_bound()
{
    var mouse = d3.pointer(event,this);
    console.log(event);

    if (exists == false)
    {
        exists = true;
        var left_line = svg
            .append("line")
            .attr("id","left_line")
            .datum({selected: false, x: 0})
            .text('left')
            .style("stroke-dasharray", ("5, 5"))
            .attr("x1", 0)
            .attr("y1", 0)
            .attr("x2", 0)
            .attr("y2", x_image(org_height))
            .attr("stroke", "red")
            .attr("stroke-width", "5px")
            .call(dragleft);
        var right_line = svg
                .append("line")
                .datum({selected: false, x: width})
                .attr("id","right_line")
                .text('right')
                .style("stroke-dasharray", ("5, 5"))
                .attr("x1", width)
                .attr("y1", 0)
                .attr("x2", width)
                .attr("y2", x_image(org_height))
                .attr("stroke", "red")
                .attr("stroke-width", "5px")
                .call(dragright);
    }
    else
    {
        d3.select("#left_line").remove();
        d3.select("#right_line").remove();
        document.getElementById('textInput2').value=0;
        document.getElementById('textInput3').value=width;
        exists = false;
    }
}



