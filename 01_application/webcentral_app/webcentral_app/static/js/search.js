const user_input = $("#search-input-tools")
const kat_input = $("#kategorie-input-tools")
const liz_input = $("#lizenz-input-tools")
const lzp_input = $("#lzp-input-tools")
const search_icon = $('#search-submit-tools')
const tool_listing_results_grid = $('#tool-listing-results')
const endpoint = '/tool_list/'
const delay_by_in_ms = 500
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            tool_listing_results_grid.fadeTo('fast', 0).promise().then(() => {
                // replace the HTML contents
                tool_listing_results_grid.html(response['html_from_view'])
                // fade-in the div with new contents
                tool_listing_results_grid.fadeTo('fast', 1)
            })
        })
}


user_input.on('keyup', function () {

    const request_parameters = {
        searched: $(this).val(), // value of user_input: the HTML element with ID user-input
        k: kat_input.val(),
        l: liz_input.val(),
        lzp: lzp_input.val()
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})