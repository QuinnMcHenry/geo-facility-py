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

    document.addEventListener("DOMContentLoaded", function () {
    const togglePanel = document.getElementById("toggle-panel");
    const leftPanel = document.getElementById("left-panel");
    const shareLocationBtn = document.getElementById("share-location");
    const closestFacilitiesList = document.getElementById("closest-facilities");
    const loadingIndicator = document.getElementById("loading");

    let userCoords = null;
    let facilities = [
        { name: "Facility A", lat: 37.7749, lon: -122.4194 },
        { name: "Facility B", lat: 34.0522, lon: -118.2437 },
        { name: "Facility C", lat: 40.7128, lon: -74.0060 },
        { name: "Facility D", lat: 41.8781, lon: -87.6298 },
        { name: "Facility E", lat: 29.7604, lon: -95.3698 }
    ]; // Example data; replace with actual facilities

    function haversineDistance(lat1, lon1, lat2, lon2) {
        const toRad = angle => (angle * Math.PI) / 180;
        const R = 6371; // Radius of Earth in km
        const dLat = toRad(lat2 - lat1);
        const dLon = toRad(lon2 - lon1);
        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    function findClosestFacilities(lat, lon) {
        loadingIndicator.style.display = "block";
        setTimeout(() => {
            const sortedFacilities = facilities
                .map(facility => ({
                    ...facility,
                    distance: haversineDistance(lat, lon, facility.lat, facility.lon)
                }))
                .sort((a, b) => a.distance - b.distance)
                .slice(0, 5);

            closestFacilitiesList.innerHTML = "";
            sortedFacilities.forEach(facility => {
                const li = document.createElement("li");
                li.textContent = `${facility.name} (${facility.distance.toFixed(2)} km)`;
                closestFacilitiesList.appendChild(li);
            });

            loadingIndicator.style.display = "none";
        }, 1500); // Simulate delay
    }

    shareLocationBtn.addEventListener("click", function () {
        if (userCoords) {
            findClosestFacilities(userCoords.lat, userCoords.lon);
        } else {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    position => {
                        userCoords = {
                            lat: position.coords.latitude,
                            lon: position.coords.longitude
                        };
                        findClosestFacilities(userCoords.lat, userCoords.lon);
                    },
                    error => alert("Location access denied.")
                );
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
    });

    togglePanel.addEventListener("click", function () {
        leftPanel.classList.toggle("open");
    });

    document.getElementById("findMe").addEventListener("click", function () {
        const address = document.getElementById("addressInput").value;
        if (address) {
            fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        userCoords = {
                            lat: parseFloat(data[0].lat),
                            lon: parseFloat(data[0].lon)
                        };
                        findClosestFacilities(userCoords.lat, userCoords.lon);
                    } else {
                        alert("Address not found.");
                    }
                });
        }
    });
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
