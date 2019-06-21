d3.json("/static/images/json1.json", function(error, graph) {
if (error) throw error;  

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = ["#6677ff","#66d691","#ffdd56","#ff6a30","#ff4242"]

var Tooltip = d3.select("svg")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

var mouseover = function(d) {
    Tooltip
      .style("opacity", 1)
}
var mousemove = function(d) {
    Tooltip
      .html('<u>' + d.id + '</u>' + "<br>" + "adverse effect")
      .style("left", (d3.mouse(this)[0]+20) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
}
var mouseleave = function(d) {
    Tooltip
      .style("opacity", 0) 
}
 
var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter().x(width / 2).y(height / 2));

var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
    .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")    
    .on("click",function(d){
          document.getElementById("search").value = d.id
          document.getElementById('search').focus()
          //var form = new Element('form',{method:'POST', action:'/test'});

          //form.insert(New Element('input',{name:'drugname',value:d.id,type:'hidden'}));
          //$(document.body).insert(form);
          //form.submit();
      })

var circles = node.append("circle")
    .attr("r", 30)
    .attr("fill", function(d) { return color[d.group-1]; })
    .style("fill-opacity", 0.8)
    .attr("stroke", "black")
    .style("stroke-width", 1)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)
    .on("mousedown", function(d) {  d.id })
    .call(d3.drag()
         .on("start", dragstarted)
         .on("drag", dragged)
         .on("end", dragended));

var lables = node.append("text")
    .text(function(d) { return d.id; })
    .attr('x', 6)
    .attr('y', 3);     

node.append("title")
    .text(function(d) { return d.id; });

simulation
    .nodes(graph.nodes)
    .on("tick", ticked);

simulation.force("link")
    .links(graph.links);

function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";})
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
});
