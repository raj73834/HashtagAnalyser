var options = {
        
    chart: {
      type: 'bar'
    },
    series: [{
      name: 'sales',
      data: {{values|safe}},
    }],
    
    xaxis: {
      categories: {{label|safe}}
    },
    fill:{
        colors: [ // this array contains different color code for each data
        "#33b2df",
        "#546E7A",
        "#d4526e",
        "#13d8aa",
        "#A5978B",
        "#2b908f",
        "#f9a3a4",
        "#90ee7e",
        "#f48024",
        "#69d2e7"
],
    }
  }
  
  var chart = new ApexCharts(document.querySelector("#chart"), options);
  
  chart.render();