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
<<<<<<< HEAD
=======

>>>>>>> 650d4e00d4659623cb87d32f78d94ee7cce91d01
// google.charts.load("current", {packages:["corechart"]});
//       google.charts.setOnLoadCallback(drawChart);
//       function drawChart() {
//         var data = google.visualization.arrayToDataTable(
//           by_typeToChartArray(by_type.data)
//         );
//         var options = {
//           title: 'My Daily Activities',
//           pieHole: 0.4,
//         };

//         var chart = new google.visualization.PieChart(document.getElementById('by_type_chart'));
//         chart.draw(data, options);
//       };

const ctx = document.getElementById('by_type_chart');
const data_and_labels = xamlon(by_type.data)
const myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: data_and_labels.labels,
        datasets: [{
            label: '# of votes',
            data: data_and_labels.data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                ],
            }
        ],
        options: {
            maintainAspectRatio: false,
            responsive: true
        }
    }
});
