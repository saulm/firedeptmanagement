google.load("maps", "2");

$(document).unload(function(){
    GUnload();
});

$(document).ready(function(){
    $("input.location_picker").each(function (i) {
        var map = document.createElement('div');
        map.className = "location_picker_map";
        this.parentNode.insertBefore(map, this);
        $(this).css('display','none');
        
        var lat = 10.431092;
        var lng = -66.873779;
        if (this.value.split(',').length == 2) {
            values = this.value.split(',');
            lat = values[0];
            lng = values[1];
        }
        var center = new GLatLng(lat,lng);

        var map = new google.maps.Map2(map);
        map.addControl(new GSmallMapControl());
        map.setCenter(center, 13);

        this.onMapClick = function(overlay, point) {
            this.value = point.lat()+','+point.lng();
            if (this.marker == null) {
                this.marker = new GMarker(point);
                this.map.addOverlay(this.marker);
            } else {
                this.marker.setPoint(point);
            }
        }

        this.marker = new GMarker(center);
        map.addOverlay(this.marker);

        GEvent.bind(map, "click", this, this.onMapClick);
    });
});