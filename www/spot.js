	var map = L.map('map').setView([45.7, -121.52], 9);
	var token = L.mapbox.accessToken = 'pk.eyJ1IjoiYndhaW5zdG9jayIsImEiOiJBMlNIQk9rIn0.6itKJwxaTteIMCyVjoWwGg';
	var map1 = L.tileLayer('http://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
	});
	var map2 = L.mapbox.tileLayer('examples.map-9d0r2yso').addTo(map);
	var map3 = L.mapbox.tileLayer('examples.map-qogxobv1');
	var campIcon = L.MakiMarkers.icon({
			icon: "campsite",
			color: "#145291",
			size: "m"
	});
	var baseIcon = L.MakiMarkers.icon({
			icon: "marker",
			color: "#3C3C43",
			size: "s"
	});
	var basicMarker = {
			radius: 5,
			color: '#333',
			fillOpacity: 1,
			stroke: false
	};
	var liveMarkerOptions = {
			radius: 5,
			color: 'white',
			fillColor: '#333',
			fillOpacity: 1,
			className: 'leaflet-marker-live'
	};

	function onEachFeature(feature, layer) {
			var myDate = new Date(feature.properties.unixtime * 1000);
			layer.bindPopup(myDate.toLocaleString());
	}

	function pointToLayer(feature, latlng) {
			switch (feature.properties.messagetype) {
			case 'UNLIMITED-TRACK':
					return L.circleMarker(latlng, basicMarker);
			case 'OK':
					return L.marker(latlng, {
							icon: campIcon
					});
			}
	}
	var pctLineStyle = {
			color: '#333',
			weight: 2,
			clickable: false,
			dashArray: '5,5'
	};
	var lineStyle = {
			color: 'red',
			weight: 4,
			opacity: 0.3
	};

	var lineJson = L.geoJson(linedata, {
			style: lineStyle
	}).addTo(map);
	var pctJson = L.geoJson(pctData, {
			style: pctLineStyle
	}).addTo(map);
	var geoJson = L.geoJson(dbdata, {
			pointToLayer: pointToLayer,
			onEachFeature: onEachFeature
	}).addTo(map);
	var overlayMaps = {
			"GeoJSON": geoJson,
			"Line": lineJson,
			"Pacific Crest Trail": pctJson
	};
	var baseMaps = {
			"Shadow": map1,
			"Bright Relief": map2,
			"Mat Relief": map3
	};
	L.control.layers(baseMaps, overlayMaps).addTo(map);
