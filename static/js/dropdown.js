// Declare markerLayer in the global scope
let markerLayer = L.layerGroup();



function myFunction(dropdownId) {
  document.getElementById(dropdownId).classList.toggle("show");
}

function filterFunction(dropdownId, inputId) {
  var input, filter, ul, li, a, i;
  input = document.getElementById(inputId);
  filter = input.value.toUpperCase();
  div = document.getElementById(dropdownId);
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function filterYear() {
  // Send a GET request to the server to filter the data by year
  fetch(`/filter?year=${year}`)
    .then(response => response.json())
    .then(data => {
      // Clear previous markers from the map
      markerLayer.clearLayers();

      // Add a marker for each result
      data.forEach(result => {
        const marker = L.marker([result[4], result[5]]);
        marker.addTo(markerLayer);

        // Bind a popup to the marker
        const popupContent = `Date: ${result[0]}<br>Persons injured: ${result[10]}<br>Persons killed: ${result[11]}<br>On Street Name: ${result[7]}<br>Cross Street Name: ${result[8]}<br>Cyclists Injured: ${result[14]}<br>Cyclists Killed: ${result[15]}<br>Motorists Injured: ${result[16]}<br>Motorists Killed: ${result[17]}<br>Pedestrians Injured: ${result[12]}<br>Pedestrians Killed: ${result[13]}`;
        marker.bindPopup(popupContent);
      });

      // Show the results on the map
      markerLayer.addTo(map);

      // Show the popup for the first result
      if (data.length > 0) {
        const firstResult = data[0];
        const firstMarker = markerLayer.getLayers()[0];
        firstMarker.openPopup();
      }
    });
}

function filterMonth(year, month) {
  // Send a GET request to the server to filter the data by month and year
  fetch(`/filter?year=${year}&month=${month}`)
    .then(response => response.json())
    .then(data => {
      // Clear previous markers from the map
      markerLayer.clearLayers();

      // Add a marker for each result
      data.forEach(result => {
        const marker = L.marker([result[4], result[5]]);
        marker.addTo(markerLayer);

        // Bind a popup to the marker
        const popupContent = `Date: ${result[0]}<br>Persons injured: ${result[10]}<br>Persons killed: ${result[11]}<br>On Street Name: ${result[7]}<br>Cross Street Name: ${result[8]}<br>Cyclists Injured: ${result[14]}<br>Cyclists Killed: ${result[15]}<br>Motorists Injured: ${result[16]}<br>Motorists Killed: ${result[17]}<br>Pedestrians Injured: ${result[12]}<br>Pedestrians Killed: ${result[13]}`;
        marker.bindPopup(popupContent);
      });

      // Show the results on the map
      markerLayer.addTo(map);

      // Show the popup for the first result
      if (data.length > 0) {
        const firstResult = data[0];
        const firstMarker = markerLayer.getLayers()[0];
        firstMarker.openPopup();
      }
    });
}


   
  
  