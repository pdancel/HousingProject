var Total = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
    "access_token=pk.eyJ1Ijoia2pnMzEwIiwiYSI6ImNpdGRjbWhxdjAwNG0yb3A5b21jOXluZTUifQ." +
    "T6YbdDixkOBWH_k9GbS8JQ"),
    Female = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
    "access_token=pk.eyJ1Ijoia2pnMzEwIiwiYSI6ImNpdGRjbWhxdjAwNG0yb3A5b21jOXluZTUifQ." +
    "T6YbdDixkOBWH_k9GbS8JQ"),
    Male = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
    "access_token=pk.eyJ1Ijoia2pnMzEwIiwiYSI6ImNpdGRjbWhxdjAwNG0yb3A5b21jOXluZTUifQ." +
    "T6YbdDixkOBWH_k9GbS8JQ");

var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 3,
    layers: [Total]
  });


d3.json("/finaldata", function(error, sampleData) {
                if (error) return console.warn(error);
                init(sampleData)
                });


function styleInfo (feature){
 return {
      opacity: 1,
      fillOpacity: 1,
      fillColor: getColor(feature.properties.ratio_total),
      //color: "#000000",
      //radius: getRadius(feature.properties.ratio_total),
      stroke: true,
      weight: 0.5
    };
  }

 // This function determines the color of the marker based on the magnitude of the earthquake.
  function getColor(ratio) {
    switch (true) {
      case ratio > 12:
        return "#bd0026";
      case ratio > 10:
        return "#f03b20";
      case ratio > 8:
        return "#fd8d3c";
      case ratio > 6:
        return "#feb24c";
      case ratio > 4:
        return "#fed976";
      case ratio > 2:
        return "#ffffb2";
      default:
        return "#ffffb2";
    }
  }

  // This function determines the radius of the earthquake marker based on its magnitude.
  // Earthquakes with a magnitude of 0 were being plotted with the wrong radius.
  function getRadius(ratio) {
    if (ratio === 0) {
      return 1;
    }

    return ratio * 4;
  }

  // Here we add a GeoJSON layer to the map once the file is loaded.
  function init(states){
    var Total = L.geoJson(states, {
       // We turn each feature into a circleMarker on the map.
       pointToLayer: function(feature, latlng) {
        return L.circleMarker(latlng,{radius:getRadius(feature.properties.ratio_total)});
      },
      // We set the style for each circleMarker using our styleInfo function.
      style: styleInfo,
      // We create a popup for each marker to display the magnitude and location of the earthquake after the marker has been created and styled
       onEachFeature: function(feature, layer) {
      
                  layer.bindPopup("<h3><strong>"+feature.properties.state+"</h3></strong><br>" + "TTL Housing - Income Ratio: "+ feature.properties.ratio_total+"<br>" +" Median Housing Price: " +feature.properties.median_home_price +"<br>"+" Median Houshold Income: " +feature.properties.combined_salary, {closeButton: false, offset: L.point(0, -20)});
                  layer.on('mouseover', function() { layer.openPopup(); });
                  layer.on('mouseout', function() { layer.closePopup(); });    
              }
     })
    var Female = L.geoJson(states, {
      // We turn each feature into a circleMarker on the map.
      pointToLayer: function(feature, latlng) {
        return L.circleMarker(latlng,{radius:getRadius(feature.properties.ratio_female)});
      },
      // We set the style for each circleMarker using our styleInfo function.
      style: styleInfo,
      // We create a popup for each marker to display the magnitude and location of the earthquake after the marker has been created and styled
       onEachFeature: function(feature, layer) {
      
                  layer.bindPopup("<h3><strong>"+feature.properties.state+"</h3></strong><br>" + "Female Housing - Income Ratio: "+ feature.properties.ratio_female+"<br>" +" Median Housing Price: " +feature.properties.median_home_price +"<br>"+" Median Female Income: " +feature.properties.female_salary, {closeButton: false, offset: L.point(0, -20)});
                  layer.on('mouseover', function() { layer.openPopup(); });
                  layer.on('mouseout', function() { layer.closePopup(); });    
              }
     })
     var Male = L.geoJson(states, {
      // We turn each feature into a circleMarker on the map.
      pointToLayer: function(feature, latlng) {
        return L.circleMarker(latlng,{radius:getRadius(feature.properties.ratio_male)});
      },
      // We set the style for each circleMarker using our styleInfo function.
      style: styleInfo,
      // We create a popup for each marker to display the magnitude and location of the earthquake after the marker has been created and styled
       onEachFeature: function(feature, layer) {
      
                  layer.bindPopup("<h3><strong>"+feature.properties.state+"</h3></strong><br>" + "Male Housing - Income Ratio: "+ feature.properties.ratio_male+"<br>" +" Median Housing Price: " +feature.properties.median_home_price +"<br>"+" Median Male Income: " +feature.properties.male_salary, {closeButton: false, offset: L.point(0, -20)});
                  layer.on('mouseover', function() { layer.openPopup(); });
                  layer.on('mouseout', function() { layer.closePopup(); });    
              }
     })
     var all = L.layerGroup([Total, Female, Male]);
  
     var baseMaps = {
      "Total": Total,
      "Female": Female,
      "Male": Male
    };
    var overlayMaps = {
      "All": all
    }
    L.control.layers(baseMaps,overlayMaps).addTo(myMap);
  }

