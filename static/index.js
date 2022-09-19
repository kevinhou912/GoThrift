
function initAutocomplete() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 30.266666, lng: -97.733330 },
    zoom: 15,
    mapTypeId: "roadmap",
  });
  
  console.log(map)
  var clicked = false;
  var infowindow = new google.maps.InfoWindow({
    maxWidth: 200
  });
  const markers = locations.map(addMarker);

  function addMarker(i){
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(i[0], i[1]),
    }); 
    marker.addListener("mouseover",
    () => {
      if (!clicked) {
        infowindow.setContent(i[2]);
        infowindow.open(map, marker);
      }
    });
    marker.addListener("mouseout",
    () => {
      if (!clicked) {
        infowindow.close();
      }
    });
    marker.addListener("clicked",
    () => {
        clicked = true;
        infowindow.setContent(i[2]);
        infowindow.open(map, marker);
      
    });
    marker.addListener("closeclick",
    () => {
        clicked = false;
      
    });
    return marker;
  }



  // Add a marker clusterer to manage the markers.
  new MarkerClusterer(map, markers, {
    imagePath:
      "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
  });

  // Create the search box and link it to the UI element.
  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  // [START maps_places_searchbox_getplaces]
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
    // Clear out the old markers.

    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }
      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });

}

const locations = [
  [ 30.266666, -97.733330,'<div><p>Savers</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg" /></div>' ],
  [ 35.266666, -106.733330 ,'<div><p>Thred Up</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 25.266666, -80.733330 ,'<div><p>My Unique</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 40.266666, -124.733330 ,'<div><p>Recycled closet</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 30.266666, -90.733330 ,'<div><p>Tradesy</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 27.266666, -140.733330 ,'<div><p>Good Will</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 28.266666, -113.733330 ,'<div><p>Dragon Fly</p><img style="height:100px;width:150px;"  src="./static/images/Thrift.png"/></div>' ],
  [ 32.266666,-105.733330 ,'<div><p>Penny Wise</p><img style="height:100px;width:150px;"  src="./static/images/Thrift.png"/></div>' ],
  [ 33.266666, -119.733330 ,'<div><p>Dollar Thrift</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 36.266666, -132.733330 ,'<div><p>Rerun</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 30.266666, -123.733330 ,'<div><p>Money grove</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 28.54356, -97.733330 ,'<div><p>Good Will</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 27.266666, -85.733330 ,'<div><p>Recycled closet</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 31.266666, -90.733330 ,'<div><p>Dollar Thrift</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 33.266666, -110.733330 ,'<div><p>Fabu finds</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 37.266666, -91.733330 ,'<div><p>Sand Dollars</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 30.266666, -120.733330 ,'<div><p>Good Will/p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 33.266666, -131.733330 ,'<div><p>Here is your image</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 28.266666, -87.733330 ,'<div><p>Thrift Store</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 29.266666, -117.733330 ,'<div><p>Good Will</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 35.266666, -116.733330 ,'<div><p>Savers</p><img style="height:100px;width:150px;" src="./static/images/Thrift.png"/></div>' ],
  [ 28.266666, -115.733330 ,'<div><p>Dollar Savers</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ],
  [ 32.266666, -106.733330 ,'<div><p>Recycled closet</p><img style="height:100px;width:150px;" src="./static/images/LogoNav.jpg"/></div>' ]
];
