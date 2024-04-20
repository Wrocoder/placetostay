async function initMap() {
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
    var hotelLat = parseFloat(document.getElementById('hotelLat').value);
    var hotelLng = parseFloat(document.getElementById('hotelLng').value);
    var hotelLocation = { lat: hotelLat, lng: hotelLng };
    var map = new google.maps.Map(document.getElementById('hotelMap'), {
        zoom: 13,
        center: hotelLocation,
        mapId: "DEMO_MAP_ID",
    });

    var marker = new google.maps.marker.AdvancedMarkerElement({
        position: hotelLocation,
        map: map
    });
}

// TODO
//Google Maps JavaScript API has been loaded directly without loading=async.
//This can result in suboptimal performance. For best-practice loading patterns please see https://goo.gle/js-api-loading

