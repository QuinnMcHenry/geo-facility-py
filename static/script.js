let map = L.map('map', {
    center: [37.0902, -95.7129], 
    zoom: 4,
    minZoom: 3,
    maxBounds: [
        [5.40, -188.29],
        [101.30, -49.49]
    ]
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

$(document).ready(function () {
    let selectedFacility = null; // Store selected facility coordinates

    // "Get Directions" button logic
    const directionsButton = document.getElementById("getDirectionsBtn");
    directionsButton.style.display = "none";

    function showDirectionsButton(lat, lng) {
        selectedFacility = { lat, lng };
        directionsButton.style.display = "block";
    }

    directionsButton.onclick = function () {
        if (!selectedFacility) return;

        const { lat, lng } = selectedFacility;

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;
                window.open(
                    `https://www.google.com/maps/dir/?api=1&origin=${userLat},${userLng}&destination=${lat},${lng}&travelmode=driving`,
                    "_blank"
                );
            }, function (error) {
                console.error("Error getting location:", error);
                alert("Location access denied. Opening Google Maps with destination only.");
                window.open(
                    `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&travelmode=driving`,
                    "_blank"
                );
            });
        } else {
            window.open(
                `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&travelmode=driving`,
                "_blank"
            );
        }
    };

    // Fetch categories
    $.getJSON('/categories', function (data) {
        let categoryDropdown = $('#category');
        categoryDropdown.append('<option>Select a category</option>');
        data.forEach(category => {
            categoryDropdown.append(`<option value="${category}">${category}</option>`);
        });
    });

    // Fetch services when category changes
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
                    map.setView([lat, lon], 10);
                } else {
                    alert("Address not found!");
                }
            })
            .catch(error => console.error("Geocoding error:", error));
    }

    let facilities = [];

    // Fetch facilities
    $.getJSON('/facility_search', function (data) {
        facilities = data;
    });

    // Search with autocomplete
    $('#facilityInput').on('input', function () {
        let query = $(this).val().toLowerCase();
        let resultsDiv = $('#facilityResults');
        resultsDiv.empty();

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
                        map.setView([facility.latitude, facility.longitude], 10);
                        L.popup()
                            .setLatLng([facility.latitude, facility.longitude])
                            .setContent(`<b>${facility.name}</b>`)
                            .openOn(map);
                        showDirectionsButton(facility.latitude, facility.longitude);
                        resultsDiv.empty();
                        $('#facilityInput').val('');
                    });
                resultsDiv.append(resultItem);
            });
        }
    });

    document.getElementById("facilityResults").addEventListener("click", function (event) {
        if (event.target.classList.contains("facility-item")) {
            document.getElementById("map").scrollIntoView({ behavior: "smooth", block: "center" });
        }
    });

    // Address search
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

    // Change facilities based on service selection
    $('#service').change(function () {
        let service = $(this).val();
        $.getJSON(`/facilities/${service}`, function (data) {
            map.eachLayer(layer => {
                if (layer instanceof L.CircleMarker) {
                    map.removeLayer(layer);
                }
            });

            data.forEach(facility => {
                let marker = L.circleMarker([facility.latitude, facility.longitude], {
                    radius: 3,
                    color: 'blue',
                    fillColor: 'blue',
                    fillOpacity: 1,
                    weight: 1
                }).addTo(map).bindPopup(facility.name);

                marker.on("click", function () {
                    showDirectionsButton(facility.latitude, facility.longitude);
                });
            });

            if (data.length > 0) {
                let bounds = L.latLngBounds(data.map(f => [f.latitude, f.longitude]));
                map.fitBounds(bounds, { maxZoom: 7 });
            }
        });
    });
});
