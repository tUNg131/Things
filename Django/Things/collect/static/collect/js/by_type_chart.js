function by_typeToChartArray(arr) {
  function _objectToArray(object) {
    var result = [object.type_name, parseInt(object.total_quantity)]
    return result
  };

  var result_array = [["Type Name", "Total Quantity"],]
  for (let i = 0; i < arr.length; i++) {
    result = _objectToArray(arr[i])
    result_array.push(result)
  };
  return result_array
};


function xamlon(arr) {
  var labels = []
  var data = []
  for (let i=0; i<arr.length; i++) {
    labels.push(arr.type_name)
    data.push(arr.total_quantity)
  }
  var result = {
    "labels": labels,
    "data": data
  }
  return result
}


google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(
          by_typeToChartArray(by_type.data)
        );
        var options = {
          title: 'My Daily Activities',
          pieHole: 0.4,
        };

        var chart = new google.visualization.PieChart(document.getElementById('by_type_chart'));
        chart.draw(data, options);
      };
