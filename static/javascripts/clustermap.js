    var map;
    var markers = [];
    var markerClusterer;
    var geocoder;
    var infowindow;
    var symptoms = {};
    var symptoms_point_array;
    var heatmap;
    var rand = 1/500.0;
    
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
    
    function populateChecklist(symptoms){
        for (var i in symptoms){
            var symptom_name = symptoms[i];
            var html = '<div><input type="checkbox" name="symptoms" value="' + symptom_name + '" checked> ' + symptom_name + '</div>';
            $("#symptom_checklist").append($(html));
        }
        $(':checkbox').change(function () {
            refreshSymptoms();
        });
        
        showPeople();
    }

    function showPeople(){
        if (!markerClusterer){
            markerClusterer = new MarkerClusterer(map, markers);
        }
        if (heatmap){
            heatmap.setMap(null);
            heatmap = null;
        }
        $("#symptom_checklist").hide();
        $("#map_title").html("People Sick in Seattle");
    }

    function showSymptoms(){
        if (!heatmap){
            buildHeatmapOfSymptom('fever');
        }
        if (markerClusterer){
            markerClusterer.clearMarkers();
            markerClusterer = null;
        }
        $("#symptom_checklist").show();
        
        $("#map_title").html("Trending Symptoms in Seattle");

    }
    
    function refreshSymptoms(){
        if (heatmap){
            heatmap.setMap(null);
            heatmap = null;
        }

        showSymptoms();
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
                one_symptom.push(new google.maps.LatLng(Number(instances[i].latitude) + Math.random()*rand - rand/2, Number(instances[i].longitude) + Math.random()*rand - rand/2));
            }
            symptoms[name] = one_symptom;
        }
    }

    function buildHeatmapOfSymptom(symptom_name){
        var selectedVal = "";
        var selected = $("#symptom_checklist div input[type='checkbox']:checked");
        if (selected.length > 0){
            var s = [];
            for (var i = 0; i < selected.length; i++){
                s.push(selected[i].value);
            }             
        }
        
        var concat_symptoms = [];
        for (i in s){
            if (symptoms[s[i]]){
                concat_symptoms = concat_symptoms.concat(symptoms[s[i]]);
            }
        }
        
    
        symptoms_point_array = new google.maps.MVCArray(concat_symptoms);
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: symptoms_point_array
        });
        heatmap.setMap(map);
    }
      
    function addPersonMarker(person){
        var latLng = new google.maps.LatLng(Number(person.latitude) + Math.random()*rand - rand/2,
              Number(person.longitude) + Math.random()*rand - rand/2);
              
              
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
