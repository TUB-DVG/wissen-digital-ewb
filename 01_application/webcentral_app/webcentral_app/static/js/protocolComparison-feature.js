function resetPageState() {
    const firstCompareButton = document.getElementById('comparisonButton');
    const comparisonBar = document.getElementById('comparisonBar');
    const inputs = document.getElementsByClassName('comparisonInput');
    const cardTitles = document.getElementsByClassName("card-title")

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].style.visibility = "hidden";
    }

    for (let i = 0; i < cardTitles.length; i++) {
        cardTitles[i].classList.remove("card-title--spaced");
    }

    firstCompareButton.style.display = '';
    comparisonBar.style.display = 'none';
    $('input[type=checkbox]').prop('checked', false);

    const elements = document.getElementsByClassName('comparison-active');

    while (elements.length) {
        elements[0].classList.remove('comparison-active');
    }

    sessionStorage.clear();
}

document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(document.location.search);

    if (!params.get('page')) {
        resetPageState();
    }

    var comparisonButtonExists = document.getElementById('comparisonButton');
    if (comparisonButtonExists) {
        $(document).ready(function () {
            // Card Multi Select
            $('input[type=checkbox]').click(function () {
                var id = $(this).parent().attr('id');
                var storedNames = JSON.parse(sessionStorage.getItem("ids")) || [];

                if ($(this).parent().hasClass('comparison-active')) {
                    $(this).parent().removeClass('comparison-active');
                    var index = storedNames.indexOf(id);
                    if (index !== -1) {
                        storedNames.splice(index, 1);
                    }
                } else {
                    $(this).parent().addClass('comparison-active');
                    storedNames.push(id);
                }

                sessionStorage.setItem("ids", JSON.stringify(storedNames));
                console.log(sessionStorage.ids);
            });
        });

        // Handling the comparison based on the session storage
        $(document).ready(function () {
            let data = sessionStorage.getItem("comparison");
            let values = JSON.parse(sessionStorage.ids) || [];
            // if session storage variable comparison is True, then the comparison should be carried over to new page
            if (data == "True") {
                comparisonButtonHandlingProtocols();
            }
            var ids = values.slice(0, -1); // Remove trailing comma
            for (let i = 0; i < ids.length; i++) {
                try {
                    var comparisonBar = document.getElementById(ids[i]);
                    var inputNode = comparisonBar.getElementsByClassName('comparisonInput')[0];
                    comparisonBar.classList.add("comparison-active");
                    inputNode.checked = true;
                } catch (e) {
                    continue;
                }
            }
        });

        // Function for handling protocols comparison
        function comparisonButtonHandlingProtocols() {
            comparisonBar.style.display = '';
            firstCompareButton.style.display = 'none';
            var inputs = document.getElementsByClassName('comparisonInput');
            for (var i = 0; i < inputs.length; i++) {
                inputs[i].style.visibility = "visible";
            }

            const cardTitles = document.getElementsByClassName("card-title")
        
            for (let i = 0; i < cardTitles.length; i++) {
                cardTitles[i].classList.add("card-title--spaced");
            }
        }

        // Define functions that describe the behaviour of the buttons for protocols comparison
        var firstCompareButton = document.getElementById('comparisonButton');
        var comparisonBar = document.getElementById('comparisonBar');
        firstCompareButton.addEventListener('click', function () {
            comparisonButtonHandlingProtocols();
            sessionStorage.setItem("comparison", "True");
        });

        // Define event listener for the second comparison button for protocols
        var secondCompareButton = document.getElementById('compareButton');
        secondCompareButton.addEventListener('click', function (event) {
            // Handle the click event for the second comparison button for protocols
            var url = document.getElementById('comparisonUrl');
            var baseUrl = "/TechnicalStandards/comparison/";
            var ids = JSON.parse(sessionStorage.ids);
            console.log(ids.length);
            if (ids.length < 2) {
                event.preventDefault();
                alert("Please select at least 2 items !!");
            } else {
                var searchParams = new URLSearchParams();
                ids.forEach(id => searchParams.append('id', id));
                url.href = baseUrl + '?' + searchParams.toString();
            }
        });

        // Define event listener for the cancel button for protocols comparison
        var cancelButton = document.getElementById('cancelButton');
        cancelButton.addEventListener('click', resetPageState);
    }
});
