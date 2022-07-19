const user_input_tools = $("#search-input-tools")
const kat_input_tools = $("#kategorie-input-tools")
const liz_input_tools = $("#lizenz-input-tools")
const lzp_input_tools = $("#lzp-input-tools")
const search_icon_tools = $('#search-submit-tools')
const tool_listing_results_grid = $('#tool-listing-results')
const endpoint_tools = '/tool_list/'
const delay_by_in_ms = 500
let scheduled_function = false

const user_input_weatherdata = $("#search-input-weatherdata")
const kat_input_weatherdata = $("#kategorie-input-weatherdata")
const liz_input_weatherdata = $("#lizenz-input-weatherdata")
const search_icon_weatherdata = $('#search-submit-tools')
const weatherdata_listing_results_grid = $('#tool-listing-results')
const endpoint_weatherdata = '/weatherdata_list/'

let ajax_call_tools = function (endpoint, request_parameters) {
    $.getJSON(endpoint_tools, request_parameters)
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


user_input_tools.on('keyup', function () {

    const request_parameters = {
        searched: $(this).val(), // value of user_input: the HTML element with ID user-input
        k: kat_input_tools.val(),
        l: liz_input_tools.val(),
        lzp: lzp_input_tools.val()
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call_tools, delay_by_in_ms, endpoint_tools, request_parameters)
})

let ajax_call_weatherdata = function (endpoint, request_parameters) {
    $.getJSON(endpoint_weatherdata, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            weatherdata_listing_results_grid.fadeTo('fast', 0).promise().then(() => {
                // replace the HTML contents
                weatherdata_listing_results_grid.html(response['html_from_view'])
                // fade-in the div with new contents
                weatherdata_listing_results_grid.fadeTo('fast', 1)
            })
        })
}


user_input_weatherdata.on('keyup', function () {

    const request_parameters = {
        searched: $(this).val(), // value of user_input: the HTML element with ID user-input
        k: kat_input_weatherdata.val(),
        l: liz_input_weatherdata.val(),
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call_weatherdata, delay_by_in_ms, endpoint_weatherdata, request_parameters)
})