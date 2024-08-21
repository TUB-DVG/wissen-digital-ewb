# Listing pages
The listing pages are an integral part of the Wissensplattform-application. They show collections of elements of different type and allow a filtering and comparison of elements. Like all parts of the website, also these pages are composed of different HTML-components. These components are 

- descriptionContainer.html
- search-bar.html:
- comparison.html
- pagination.html

On specific listing sites it is possible to show a comparison of different elements. 

In the following section the implementation of these pages is described in detail.

## Technical implementation
The listing-sites have a features implemented, which are described in that section. These features are the asynchronious loading of filtered elements and the comparison-feature.

### Asynchronious loading of filtered elements
When selecting filters or entering a search string into the search-bar, a asynchronious javascript and XML (ajax)-request is sent from the browser to the django-backend to retrive the filtered listing items:
```
$('#searchBox').on('submit', function(e) {
    e.preventDefault();  // Prevent the form from submitting normally

    var url = $(this).attr('action');  // Get the form's action URL
    var formData = $(this).serialize();  // Serialize the form data

    $.ajax({
        type: 'GET',
        url: url,
        data: formData,
        success: function(response) {
            // Handle the response here
            // remove all ancestors of the div with the id
            if ($("#componentListingContainer").length > 0) {
              $('#componentListingContainer').empty();
              $('#componentListingContainer').append(response);
            }
            else if ($('#tool-listing-results').length > 0) {
              $('#tool-listing-results').empty();
              $('#tool-listing-results').append(response);
            }
            else if ($("#dataset-listing-results").length > 0) {
              $('#dataset-listing-results').empty();
              $('#dataset-listing-results').append(response);             
            }
            else if ($("#weatherdata-listing-results").length > 0) {
              $('#weatherdata-listing-results').empty();
              $('#weatherdata-listing-results').append(response);             
            }
            else if ($("#protocol-listing-results").length > 0) {
              $('#protocol-listing-results').empty();
              $('#protocol-listing-results').append(response);             
            }
            else if ($("#norm-listing-results").length > 0) {
              $('#norm-listing-results').empty();
              $('#norm-listing-results').append(response);             
            }
          },
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle the error here
        }
    });
});
```
(From search-bar.html)
In the above javascript code, a ajax GET-request is performed, whereby the filter from-data is put into the request and sent to the backend, where the filtering is performed. As a response a HTML partial is returned, which is put at the position in the DOM, where the listed elements shuld be present.

### Comparison feature
The implementation of the comparison feature is descibed in the following.
