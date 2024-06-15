#!/usr/bin/node
// Listen for changes on each input checkbox tag
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
});
