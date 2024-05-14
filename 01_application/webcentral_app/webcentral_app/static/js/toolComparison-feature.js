document.addEventListener('DOMContentLoaded', function () {
    var firstComparisonButtonToolsExists = document.getElementById('firstComparisonButtonTools');
    if (firstComparisonButtonToolsExists) {
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
            let data = sessionStorage.getItem("comparisonTools");
            let values = JSON.parse(sessionStorage.ids) || [];
            // if session storage variable comparison is True, then the comparison should be carried over to new page
            if (data == "True") {
                comparisonButtonHandlingTools();
            }
            var ids = values.slice(0, -1); // Remove trailing comma
            for (let i = 0; i < ids.length; i++) {
                try {
                    var comparisonBar = document.getElementById(ids[i]);
                    var inputNode = comparisonBar.getElementsByClassName('comparisonInputTools')[0];
                    comparisonBar.classList.add("comparison-active");
                    inputNode.checked = true;
                } catch (e) {
                    continue;
                }
            }
        });

        function comparisonButtonHandlingTools() {
            comparisonBarTools.style.display = '';
            firstComparisonButtonTools.style.display = 'none';
            var inputs = document.getElementsByClassName('comparisonInputTools');
            for (var i = 0; i < inputs.length; i++) {
                inputs[i].style.visibility = "visible";
            }

            const cardTitles = document.getElementsByClassName("card-title")
        
            for (let i = 0; i < cardTitles.length; i++) {
                cardTitles[i].classList.add("card-title--spaced");
            }
        }

        // Define functions that describe the behaviour of the buttons for tools comparison
        var firstComparisonButtonTools = document.getElementById('firstComparisonButtonTools');
        var comparisonBarTools = document.getElementById('comparisonBarTools');
        firstComparisonButtonTools.addEventListener('click', function () {
            sessionStorage.clear();
            comparisonButtonHandlingTools();
            sessionStorage.setItem("comparisonTools", "True");
        });

        // Define event listener for the second comparison button for tools
        var secondComparisonButtonTools = document.getElementById('secondComparisonButtonTools');
        secondComparisonButtonTools.addEventListener('click', function (event) {
            // Handle the click event for the second comparison button for tools
            var url = document.getElementById('comparisonUrlTools');
            var baseUrl = "/common/comparison/";
            var ids = JSON.parse(sessionStorage.ids);
            console.log(ids.length);
            if (ids.length < 2) {
                event.preventDefault();
                alert("Please select at least 2 items !!");
            } else {
                var searchParams = new URLSearchParams();
                ids.forEach(id => searchParams.append('id', id));
                searchParams.append('model', modelName);
                url.href = baseUrl + '?' + searchParams.toString();
            }
        });

        // Define event listener for the cancel button for tools comparison
        var cancelButtonTools = document.getElementById('cancelButtonTools');
        cancelButtonTools.addEventListener('click', function () {
            // Reset the comparison interface for tools
            var inputs = document.getElementsByClassName('comparisonInputTools');
            for (var i = 0; i < inputs.length; i++) {
                inputs[i].style.visibility = "hidden";
            }

            const cardTitles = document.getElementsByClassName("card-title")

            for (let i = 0; i < cardTitles.length; i++) {
                cardTitles[i].classList.remove("card-title--spaced");
            }

            firstComparisonButtonTools.style.display = '';
            comparisonBarTools.style.display = 'none';
            $('input[type=checkbox]').prop('checked', false);
            var elements = document.getElementsByClassName('comparison-active');
            while (elements.length) {
                elements[0].classList.remove('comparison-active');
            }
            sessionStorage.clear();
        });
    }
});
