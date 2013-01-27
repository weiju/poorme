    var map;
    var markers = [];
    var markerClusterer;
    var geocoder;
    var infowindow;
    
    
    function initialize() {
        var mapOptions = {
            center: new google.maps.LatLng(47.652421, -122.310376),
            zoom: 8,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
            
        geocoder = new google.maps.Geocoder();
        populateMap();
    }
      
    function populateMap(){
        for (var i = 0; i < data.people.length; i++){
            var person = data.people[i];
            addPersonMarker(person);
        }
        
        markerClusterer = new MarkerClusterer(map, markers);
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
                content: person.name + " says: " + person.status + "<br /><a href='" + person.wall_url + "'>view wall</a>"
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
