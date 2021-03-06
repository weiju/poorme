    var map;
    var markers = [];
    var markerClusterer;
    var geocoder;
    var infowindow;
    var symptoms = {};
    var symptoms_point_array;
    var heatmap;
    var rand = 1/500.0;
    var cityName = "Seattle"

    function initialize(data) {
        var mapOptions = {
            center: new google.maps.LatLng(47.652421, -122.310376),
            zoom: 10,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

        $.ajax({
            type: "GET",
            url: "http://api.ipinfodb.com/v3/ip-city/?key=139a60d81999b3025d9fc13d412ae7f3997ff110cace95b1505fb72258aaef64&format=json",
            dataType: "jsonp",
            success: centerMap
        })
 
        geocoder = new google.maps.Geocoder();
        populateMap(data);
    }

    function centerMap(data){    
        map.setCenter(new google.maps.LatLng(data.latitude, data.longitude));
        cityName = data.cityName + " (" + data.zipCode + ")";
        showSymptoms();
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
        $("#map_title").html("People Sick in " + cityName);
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
        
        $("#map_title").html("Trending Symptoms in " + cityName);

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
            data: symptoms_point_array,
            gradient: [
                'rgba(0, 255, 255, 0)',
                'rgba(0, 255, 255, 1)',
                'rgba(0, 191, 255, 1)',
                'rgba(0, 127, 255, 1)',
                'rgba(0, 63, 255, 1)',
                'rgba(0, 0, 255, 1)',
                'rgba(0, 0, 223, 1)',
                'rgba(0, 0, 191, 1)',
                'rgba(0, 0, 159, 1)',
                'rgba(0, 0, 127, 1)',
                'rgba(63, 0, 91, 1)',
                'rgba(127, 0, 63, 1)',
                'rgba(191, 0, 31, 1)',
                'rgba(255, 0, 0, 1)'
              ]
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
