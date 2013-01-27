    var map;
    var markers = [];
    var markerClusterer;
    var geocoder;
    var infowindow;
    var symptoms = {};
    var symptoms_point_array;
    var heatmap;
    
    function initialize(data) {
        var mapOptions = {
            center: new google.maps.LatLng(47.652421, -122.310376),
            zoom: 8,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
            
        geocoder = new google.maps.Geocoder();
        populateMap(data);
    }
      
    function populateMap(data){
        for (var i = 0; i < data.statuses.length; i++){
            var person = data.statuses[i];
            addPersonMarker(person);
        }

        for (var name in data.symptoms){
            var instances = data.symptoms[name];
            var one_symptom = [];
            for (var i = 0; i < instances.length; i++){
                one_symptom.push(new google.maps.LatLng(instances[i].latitude, instances[i].longitude));
            }
            symptoms[name] = one_symptom;
        }

        buildHeatmapOfSymptom('fever');

        
        markerClusterer = new MarkerClusterer(map, markers);
        //markerClusterer.setMap(null);
    }

    function buildHeatmapOfSymptom(symptom_name){
        symptoms_point_array = new google.maps.MVCArray(symptoms[symptom_name]);
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: symptoms_point_array
        });
        heatmap.setMap(map);
    }
      
    function addPersonMarker(person){
        var latLng = new google.maps.LatLng(person.latitude,
              person.longitude);
              
              
        var marker = new google.maps.Marker({
            position: latLng,
            draggable: false,
        });
        
        
        
        markers.push(marker);
        
        google.maps.event.addListener(marker, 'click', function() {
            if (infowindow) infowindow.close();

            infowindow = new google.maps.InfoWindow({
                content: person.name + " says: " + person.status + "<br /><a href='" + person.url + "'>view wall</a>"
            });
            infowindow.open(map, this);
        });   
    }
    
    //Call this wherever needed to actually handle the display
    function codeAddress(zipCode) {
        geocoder.geocode( { 'address': zipCode}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                //Got result, center the map and put it out there
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
            });
            } else {
                alert("Geocode was not successful for the following reason: " + status);
            }
        });
    }
