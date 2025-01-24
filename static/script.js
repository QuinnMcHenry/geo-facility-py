let map = L.map('map').setView([37.0902, -95.7129], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
$(document).ready(function () {
	$.getJSON('/categories', function (data) {
		let categoryDropdown = $('category');
		categoryDropdown.append('<option>Select a category</option>');
		data.forEach(category => {
			categoryDropdowm.append(`<option value="${category}">${category}</option>`);
		});
	});

	$('#category').change(function () {
		let category = $(this).val();
		$('#service').empty().append('<option>Select a service</option>);

		$.getJSON(`/services/${category}`, function (data) {
			data.forEach(service => {
				$('#service').append(<option value="${service}"></option>);
			});
		});
	});
	
	$('#service').change(function () {
		let service = $(this).val();
		$.getJSON(`/facilities/${service}`, function (data) {
			map.eachLayer(layer => {
				if (layer instanceof L.CircleMarker) {
					map.removeLayer(layer);
				}
			});
			
			data.forEach(facility => {
				L.circleMarker([facility.latitude, facility.longitude], {
					radius: 5,
					color:"blue"
				}).addTo(map).bindPopup(facility.name);
			});
		});
	});
});
