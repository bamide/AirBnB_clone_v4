#!/usr/bin/node
// Filter places by Amenity
$(document).ready(function () {
  const checkedAmenities = {};

  $('input[type="checkbox"]').change(function () {
    if (this.checked) {
      checkedAmenities[$(this).data('id')] = $(this).data('name');
    } else {
      delete checkedAmenities[$(this).data('id')];
    }

    const amenitiesList = Object.values(checkedAmenities).join(', ');
    $('.amenities h4').text(amenitiesList);
  });

  // Fetch places with filters
  function fetchPlacesWithFilters() {
    const amenityIds = Object.keys(checkedAmenities);
    $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ amenities: amenityIds }),
      success: function (places) {
        $('.places').empty();
        places.forEach(place => {
          const placeHtml = `
            <article>
              ...
            </article>
          `;
          $('.places').append(placeHtml);
        });
      }
    });
  }

  // Fetch places initially
  fetchPlacesWithFilters();

  // Fetch places on button click
  $('button').click(function () {
    fetchPlacesWithFilters();
  });
});
