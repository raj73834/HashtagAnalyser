// import jsonData from "./new_list.json"

// const jsonData =require("/home/fxdata/Downloads/insta/vscode for insta/Folder for one file/Hastag/static/js/pages/plugins/json_files/new_list.json");
// console.log("print here list",jsonData)

// const xLabel  = ["Positive","Neutral","Negative"]
// console.log(one_user_details.data)

function getChartColorsArray(e) {
    
    if (null !== document.getElementById(e)) {
        var t = document.getElementById(e).getAttribute("data-colors");
        if (t)
            return (t = JSON.parse(t)).map(function (e) {
                var t = e.replace(" ", "");
                if (-1 === t.indexOf(",")) {
                    var r = getComputedStyle(document.documentElement).getPropertyValue(t);
                    return r || t;
                }
                e = e.split(",");
                return 2 != e.length ? t : "rgba(" + getComputedStyle(document.documentElement).getPropertyValue(e[0]) + "," + e[1] + ")";
            });
        console.warn("data-colors Attribute not found on:", e);
    }
}
var areachartSalesColors = getChartColorsArray("sales-forecast-chart");
areachartSalesColors &&
    ((options = {
        series: chart_data,
        chart: { type: "bar", height: 450, toolbar: { show: !0 } },
        plotOptions: { bar: { horizontal: !1, columnWidth: "60%" } },
        stroke: { show: !0, width: 10, colors: ["transparent"] },
        xaxis: {
            categories: [""],
            axisTicks: { show: !1, borderType: "solid", color: "#78909C", height: 6, offsetX: 0, offsetY: 0 },
            // title: { text: "Total Forecasted Value", offsetX: 0, offsetY: -30, style: { color: "#78909C", fontSize: "12px", fontWeight: 400 } },
        },
        yaxis: {
            labels: {
                formatter: function (e) {
                    return e;
                },
            },
            tickAmount: 4,
            min: 0,
        },
        fill: { opacity: 1 },
        legend: { show: !0, position: "bottom", horizontalAlign: "center", fontWeight: 500, offsetX: 0, offsetY: -14, itemMargin: { horizontal: 8, vertical: 0 }, markers: { width: 13, height: 13 } },
        colors: areachartSalesColors,
    }),
    (chart = new ApexCharts(document.querySelector("#sales-forecast-chart"), options)).render());


var chartStackedBarColors = getChartColorsArray("stacked_bar");
chartStackedBarColors &&
    ((options = {
        series: [
            // { name: "16 hours ago", data: [1366] },
            // { name: "14 hours ago", data: [981] },
            // { name: "2 hours ago", data: [6492] },
            // { name: "17 hours ago", data: [823] },
            // { name: "13 hours ago", data: [2737] },
            // { name: "13 hours ago", data: [869,854,896,675] },
            // { name: "8 hours ago", data: [88024] },
            { name: "3 hours ago", data: [340] },
            { name: "20 hours ago", data: [0] },
            { name: "4 minutes ago", data: [2] },
            { name: "4 minutes ago", data: [0] },
            { name: "4 minutes ago", data: [0] },
            { name: "4 minutes ago", data: [2] },
            { name: "4 minutes ago", data: [1] },
            { name: "6 minutes ago", data: [0] },
            { name: "6 minutes ago", data: [82] },
        ], 
        
        chart: { type: "bar", height: 600, stacked: false, toolbar: { show: true },},
        plotOptions: { bar: { horizontal: false } }, // chang in horizontal !0
        stroke: { width: 1, colors: ["#fff"] },
        title: { text: "Fiction Books Sales", style: { fontWeight: 500 } },
        xaxis: {
            categories: [""],

            // labels: {
            //     formatter: function (t) {
            //         return t + "K";
            //     },
            // },
        },
        yaxis: { title: { text: void 0 } },
        // tooltip: {
        //     y: {
        //         formatter: function (t) {
        //             return t + "K";
        //         },
        //     },
        // },
        fill: { opacity: 1 },
        legend: { position: "bottom" },
        colors: chartStackedBarColors,
    }),
    (chart = new ApexCharts(document.querySelector("#stacked_bar"), options)).render());



var chartDonutBasicColors = getChartColorsArray("simple_dount_chart");
chartDonutBasicColors &&
    ((options = {
        series: for_freq, chart: { height: 500, type: "donut" },
    labels: for_lang, legend: { position: "bottom" }, 
    dataLabels: { dropShadow: { enabled: !1 } }, colors: chartDonutBasicColors }),
    (chart = new ApexCharts(document.querySelector("#simple_dount_chart"), options)).render());


var chartDonutBasicColors = getChartColorsArray("freq_user");
chartDonutBasicColors &&
    ((options = {
        series: users_count, chart: { height: 500, type: "donut" },
    labels: users_name, legend: { position: "bottom" },
    dataLabels: { dropShadow: { enabled: !1 } }, colors: chartDonutBasicColors }),
    (chart = new ApexCharts(document.querySelector("#freq_user"), options)).render());


var chartStackedBarColors = getChartColorsArray("one_user_chart");
chartStackedBarColors &&
    ((options = chartoption(one_user_details_1)
    ),

    
    (chart = new ApexCharts(document.querySelector("#one_user_chart"), options)).render()
    );
    // console.log(one_user_details_1)

    const changedata = document.getElementById('changeData');
    changedata.addEventListener('change',function(e){
        let currentChart = e.target.value ? e.target.value : 1;
        let optionArr = [
            one_user_details_1,
            one_user_details_2,
            one_user_details_3,
            one_user_details_4,
            one_user_details_5,
            // console.log(one_user_details_1)
        ]
        let optionchart = optionArr[currentChart-1]

        document.querySelector("#one_user_chart").innerHTML = '';
        options = chartoption(optionchart)
        chart = new ApexCharts(document.querySelector("#one_user_chart"), options).render()
        // console.log(optionchart)
    });

    function chartoption(option){
        return {series: option,        
            chart: { type: "bar", height: 480, stacked: false, toolbar: { show: true }, },
            plotOptions: { bar: { horizontal: false, columnWidth: '60%'} }, // chang in horizontal !0
            stroke: { show: true, width: 7, colors: ["transparent"] },
            title: { text: "This is the only one user's details.", style: { fontWeight: 500 } },
    
            dataLabels:{
                style:{
                    colors:['#06333b']
                }
            },
            xaxis: {
                categories: [""],
    
                // labels: {
                //     formatter: function (t) {
                //         return t + "K";
                //     },
                // },
            },
            yaxis: { title: { text: void 0,} },
            // tooltip: {
            //     y: {
            //         formatter: function (t) {
            //             return t + "K";
            //         },
            //     },
            // },
            tooltip: {
                custom: function({seriesIndex, dataPointIndex, w}) {
                  var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
                  
                  return '<ul>' +
                  '<li><b>Userid</b>: ' + data.userid + '</li>' +
                  '<li><b>Time</b>: ' + data.x + '</li>' +
                  '<li><b>Number of Likes</b>: ' + data.y + '</li>' +
                  '<li><b>Sentiments</b>: ' + data.sentiment + '</li>' +
                  '<li><b>Language</b>: ' + data.language + '</li>' +
                //   '<li><b>Site</b>: \'' + data.site + '\'</li>' +
                  '</ul>';
                }
              },
            fill: { opacity: 1 },
            legend: { position: "bottom" },
            colors: chartStackedBarColors,}
            
    }    


var dealTypeChartsColors = getChartColorsArray("deal-type-charts");
dealTypeChartsColors &&
    ((options = {
        series: [
            { name: "Pending", data: [80, 50, 30, 40, 100, 20] },
            { name: "Loss", data: [20, 30, 40, 80, 20, 80] },
            { name: "Won", data: [44, 76, 78, 13, 43, 10] },
        ],
        chart: { height: 341, type: "radar", dropShadow: { enabled: !0, blur: 1, left: 1, top: 1 }, toolbar: { show: !1 } },
        stroke: { width: 2 },
        fill: { opacity: 0.2 },
        legend: { show: !0, fontWeight: 500, offsetX: 0, offsetY: -8, markers: { width: 8, height: 8, radius: 6 }, itemMargin: { horizontal: 10, vertical: 0 } },
        markers: { size: 0 },
        colors: dealTypeChartsColors,
        xaxis: { categories: ["2016", "2017", "2018", "2019", "2020", "2021"] },
    }),
    (chart = new ApexCharts(document.querySelector("#deal-type-charts"), options)).render());
var options,
    chart,
    revenueExpensesChartsColors = getChartColorsArray("revenue-expenses-charts");
revenueExpensesChartsColors &&
    ((options = {
        series: [
            { name: "Revenue", data: [20, 25, 30, 35, 40, 55, 70, 110, 150, 180, 210, 250] },
            { name: "Expenses", data: [12, 17, 45, 42, 24, 35, 42, 75, 102, 108, 156, 199] },
        ],
        chart: { height: 290, type: "area", toolbar: "false" },
        dataLabels: { enabled: !1 },
        stroke: { curve: "smooth", width: 2 },
        xaxis: { categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] },
        yaxis: {
            labels: {
                formatter: function (e) {
                    return "$" + e + "k";
                },
            },
            tickAmount: 5,
            min: 0,
            max: 260,
        },
        colors: revenueExpensesChartsColors,
        fill: { opacity: 0.06, colors: revenueExpensesChartsColors, type: "solid" },
    }),
    (chart = new ApexCharts(document.querySelector("#revenue-expenses-charts"), options)).render());
