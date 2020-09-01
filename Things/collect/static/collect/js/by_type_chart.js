import {convertJSONToArray} from convert_JSON_to_array.js;

var public_data = {
  'by_type': '[{"type_name": "Nh\\u1ef1a", "total_quantity": 21}, {"type_name": "Gi\\u1ea5y", "total_quantity": 17}, {"type_name": "S\\u1eaft", "total_quantity": 10}, {"type_name": "Niken", "total_quantity": 10}, {"type_name": "H\\u1ee3p kim", "total_quantity": 5}, {"type_name": "Inox", "total_quantity": 5}, {"type_name": "Nh\\u00f4m", "total_quantity": 4}, {"type_name": "Linh ki\\u1ec7n \\u0111i\\u1ec7n t\\u1eed c\\u00e1c lo\\u1ea1i", "total_quantity": 3}, {"type_name": "Ch\\u00ec", "total_quantity": 1}]',
  'by_month': '[{"month": null, "year": null, "total_quantity": 78}]'
}

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


by_type = JSON.parse(public_data.by_type);
var result = convert(by_type);

var chartLabels = result.labels;
var chartData = result.values;

const ctx = document.getElementById('by_type_chart');
const data_and_labels = xamlon(by_type.data)
const myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: chartLabel,
        datasets: [{
            label: 'Số liệu về rác tái chế',
            data: chartData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(66, 239, 245, 0.8)',
                'rgba(43, 65, 255, 0.8)',
                'rgba(196, 33, 80, 0.8)',
                ],
            }
        ],
        options: {
            maintainAspectRatio: false,
            responsive: true
        }
    }
});
