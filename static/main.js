
  function updateTable() {
    $.ajax({
        url: 'http://10.40.9.25:8001/api/v2/get/all/plant',
        method: 'GET',
        success: function(data) {
            // Update table rows
            var tbody = $('#plantTable tbody');
            tbody.empty();
            data.forEach(function(item) {
                var row = '<tr>' +
                    '<td>' + item.plant_id + '</td>' +
                    '<td>' + item.name + '</td>' +
                    '<td>' + item.pin_soil.pin_value + '</td>' +
                    '<td>' + item.capacity + '</td>' +
                    '</tr>';
                tbody.append(row);
            });
        }
    });
}

// Call updateTable function every second
setInterval(updateTable, 300);


 // JavaScript code
 document.addEventListener('DOMContentLoaded', function() {
    // Loop through all soil chart canvas elements
    document.querySelectorAll('canvas[id^="soilChart"]').forEach(function(canvas, index) {
        var ctx = canvas.getContext('2d');
        var soilValue = parseFloat(canvas.getAttribute('data-soil-value')); // Get soil value from data attribute
        var dryValue = 100 - soilValue;
        var soilChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    label:  ['Влажность'],
                    data: [soilValue, dryValue], // Values for wet and dry percentages
                    backgroundColor: [
                        'rgb(64, 224, 208)',
                        'rgb(150, 222, 209)'
                    ],
                    borderWidth: 1
                }]
            },

            options: {
                cutoutPercentage: 80, // Create a half pie chart
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: false,
                    text: 'Влажность'
                },
                animation: {
                    animateRotate: true,
                    animateScale: true
                }
            }
        });
    });

    // Toggle pump state
    var pumpCircle = document.querySelector('.pump');
    // Check pump state on page load
    if (document.getElementById('pumpState').value === 'true') {
        pumpCircle.classList.add('active');
    }

    document.querySelectorAll('.device').forEach(function(device) {
        device.addEventListener('click', function() {
            // Toggle 'active' class on the clicked device if it's the pump
            if (device.classList.contains('pump')) {
                device.classList.toggle('active');
                document.getElementById('pumpState').value = device.classList.contains('active') ? 'true' : 'false';
            }
        });
    });

    var pumpCircle = document.querySelector('.relay');
    // Check pump state on page load
    if (document.getElementById('relayState').value === 'true') {
        pumpCircle.classList.add('active');
    }

    document.querySelectorAll('.device').forEach(function(device) {
        device.addEventListener('click', function() {
            // Toggle 'active' class on the clicked device if it's the pump
            if (device.classList.contains('relay')) {
                device.classList.toggle('active');
                document.getElementById('relayState').value = device.classList.contains('active') ? 'true' : 'false';
            }
        });
    });
});
