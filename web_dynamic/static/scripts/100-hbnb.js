#!/usr/bin/node
$(document).ready(function () {
  const checkedAmenities = {};
  const checkedStatesCities = {};

  // Listen to changes on each input checkbox tag
  $('input[type="checkbox"]').change(function () {
    if ($(this).hasClass('amenity_checkbox')) {
      // If the checkbox is an amenity
      if (this.checked) {
        checkedAmenities[$(this).data('id')] = $(this).data('name');
      } else {
        delete checkedAmenities[$(this).data('id')];
      }
    } else if ($(this).hasClass('state_city_checkbox')) {
      // If the checkbox is a state or city
      if (this.checked) {
        checkedStatesCities[$(this).data('id')] = $(this).data('name');
      } else {
        delete checkedStatesCities[$(this).data('id')];
      }
    }

    // Update the h4 tag inside the div Locations with the list of States or Cities checked
    const statesCitiesList = Object.values(checkedStatesCities).join(', ');
    $('.locations h4').text(statesCitiesList);
  });

  // Handle button click event
  $('button').click(function () {
    // Prepare data for the POST request
    const amenityIds = Object.keys(checkedAmenities);
    const stateCityIds = Object.keys(checkedStatesCities);

    // Make a new POST request to places_search
    $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        amenities: amenityIds,
        states_cities: stateCityIds
      }),
      success: function (places) {
        // Handle successful response
        $('.places').empty();
        places.forEach(place => {
          // Render each place
          const placeHtml = `
            <article>
              ...
            </article>
          `;
          $('.places').append(placeHtml);
        });
      },
      error: function (xhr, status, error) {
        // Handle error response
        console.error(error);
      }
    });
  });
});
