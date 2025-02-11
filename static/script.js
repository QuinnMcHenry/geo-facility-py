let map = L.map('map', {
    center: [37.0902, -95.7129], 
    zoom: 4,
    minZoom: 3,  // zoom limit 
    maxBounds: [  // drag limit
        [5.40, -188.29],  // Southwest corner
        [101.30, -49.49]  // Northeast corner
    ]
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

$(document).ready(function () {
    // Load categories
    $.getJSON('/categories', function (data) {
        let categoryDropdown = $('#category');
        categoryDropdown.append('<option>Select a category</option>');
        data.forEach(category => {
            categoryDropdown.append(`<option value="${category}">${category}</option>`);
        });
    });

    // get associated services when category changes
    $('#category').change(function () {
        let category = $(this).val();
        $('#service').empty().append('<option>Select a service</option>');

        $.getJSON(`/services/${category}`, function (data) {
            data.forEach(service => {
                $('#service').append(`<option value="${service}">${service}</option>`);
            });
        });
    });

function geocodeAddress(address) {
    let url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                let lat = parseFloat(data[0].lat);
                let lon = parseFloat(data[0].lon);
                map.setView([lat, lon], 10);  // Zoom in to the location
            } else {
                alert("Address not found!");
            }
        })
        .catch(error => console.error("Geocoding error:", error));
}

let facilities = [];

// Fetch all facilities for search
$.getJSON('/facility_search', function (data) {
    facilities = data;
});

// Search functionality
$('#facilityInput').on('input', function () {
    let query = $(this).val().toLowerCase();
    let resultsDiv = $('#facilityResults');
    resultsDiv.empty(); // Clear previous results

    if (query.length > 1) {
        let seenFacilities = new Set();
        let matches = facilities.filter(facility =>  {
            if (facility.name.toLowerCase().includes(query) && !seenFacilities.has(facility.name)) {
                seenFacilities.add(facility.name);
                return true;
            }
            return false;
        });

        matches.forEach(facility => {
            let resultItem = $('<div class="facility-item"></div>')
                .text(facility.name)
                .click(() => {
                    map.setView([facility.latitude, facility.longitude], 10);  // Zoom to facility
                    L.popup()
                        .setLatLng([facility.latitude, facility.longitude])
                        .setContent(`<b>${facility.name}</b>`)
                        .openOn(map);
                    resultsDiv.empty();  // Clear search results
                    $('#facilityInput').val('');  // Reset input field
                });
            resultsDiv.append(resultItem);
        });
    }
});


// address finder
$('#findMe').click(() => {
    let address = $('#addressInput').val();
    if (address) {
        geocodeAddress(address);
    } else {
        alert("Please enter an address.");
    }
});

$('#addressInput').keypress((event) => {
    if (event.which === 13) {
        $('#findMe').click();
    }
});
    // change facilities on new service
    $('#service').change(function () {
        let service = $(this).val(); // service name str
        $.getJSON(`/facilities/${service}`, function (data) {
            map.eachLayer(layer => {
                if (layer instanceof L.CircleMarker) {
                    map.removeLayer(layer); // if layer has markers, remove them
                }
            });

            data.forEach(facility => {
                L.circleMarker([facility.latitude, facility.longitude], {
                    radius: 3,
                    color: 'blue',
                    fillColor: 'blue',
		    fillOpacity: 1,
		    weight: 1	
                }).addTo(map).bindPopup(facility.name);
            });

	    if (data.length > 0) {
		let bounds = L.latLngBounds(data.map(f => [f.latitude, f.longitude]));
		map.fitBounds(bounds, { maxZoom: 7 });
	    }
        });
    });
});

