function convert(arr) {
    var labels = []
    var values = []
    for (let i = 0; i < arr.length; i++) {
        labels.push(arr[i].type_name)
        values.push(arr[i].total_quantity)
    }
    var result = {
        "labels": labels,
        "values": values
    }
    return result
}


// đây là cái JSON cần convert to array
var public_data = {
    'by_type': '[{"type_name": "Nh\\u1ef1a", "total_quantity": 21}, {"type_name": "Gi\\u1ea5y", "total_quantity": 17}, {"type_name": "S\\u1eaft", "total_quantity": 10}, {"type_name": "Niken", "total_quantity": 10}, {"type_name": "H\\u1ee3p kim", "total_quantity": 5}, {"type_name": "Inox", "total_quantity": 5}, {"type_name": "Nh\\u00f4m", "total_quantity": 4}, {"type_name": "Linh ki\\u1ec7n \\u0111i\\u1ec7n t\\u1eed c\\u00e1c lo\\u1ea1i", "total_quantity": 3}, {"type_name": "Ch\\u00ec", "total_quantity": 1}]',
    'by_month': '[{"month": null, "year": null, "total_quantity": 78}]'
}
// ở đây by_month bị lỗi tôi chỉ chuyển by_type 

// phải parse sang dạng JSON trước khi xử lý
by_type = JSON.parse(public_data.by_type);
var result = convert(by_type);

var arr1 = result.labels;
var arr2 = result.values;

// đây là cái tôi đang try
// let getDataFromJSON = Object.entries(public_data);

// console.log(getDataFromJSON);

console.log(arr1)
console.log(arr2)


//dạng array expected output
// var arr1 = ['niken', 'Hop kim', 'Inox']
// var arr2 = [13, 22, 36,]