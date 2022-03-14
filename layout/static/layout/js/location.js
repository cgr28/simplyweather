// location.js
// all logic for retrieving locations on click

function getLocation() {

    disableButton()

    city = document.querySelector("#city");
    state = document.querySelector("#state");
    ctry = document.querySelector("#ctry");

    if (city.value) {
        reference = 'weather/current/?city=' + city.value;
        if (state.value) {
            reference = reference + "&state=" + state.value;
        }
        if (ctry.value) {
                reference = reference + "&ctry=" + ctry.value;
        }
        window.location.href = reference;
    } else {
        window.location.href = '/?error=lookup';
    }
}

// prevents users from using after submission
function disableButton() {
    attribute = document.createAttribute('disabled');
    document.querySelector("#ctry").setAttributeNode(attribute)
    attribute = document.createAttribute('disabled');
    document.querySelector("#city").setAttributeNode(attribute)
    attribute = document.createAttribute('disabled');
    document.querySelector("#state").setAttributeNode(attribute)
    bttn = document.querySelector('#go');
    bttn2 = document.querySelector('#location-bttn');
    bttn.innerHTML = "<span class='spinner-border spinner-border-sm'></span>";
    bttn2.disabled = true;
    bttn.disabled = true;
}

function getCurrentLocation()
{
    attribute = document.createAttribute('disabled');
    document.querySelector("#ctry").setAttributeNode(attribute)
    attribute = document.createAttribute('disabled');
    document.querySelector("#city").setAttributeNode(attribute)
    attribute = document.createAttribute('disabled');
    document.querySelector("#state").setAttributeNode(attribute)
    bttn = document.querySelector('#location-bttn');
    bttn2 = document.querySelector('#go');
    bttn.innerHTML = "<span class='spinner-border spinner-border-sm'></span>";
    bttn2.disabled = true;
    bttn.disabled = true;
    function success(position) {
        const latitude  = position.coords.latitude;
        const longitude = position.coords.longitude;
        window.location.href = 'weather/current/?lat=' + latitude + "&long=" + longitude;
        return false;
    }

    // loads home page with an location error
    function error() {
        window.location.href = '/?error=location';
    }

    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(success, error);
    }

}




bttn = document.querySelector('#location-bttn');
btt2 = document.querySelector('#go');
search = document.querySelectorAll(".searchbar");

for (i = 0; i < search.length; i++) {
    search[i].addEventListener("keyup", function(event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("go").click();
    }
    });
}


btt2.addEventListener("click", getLocation);
bttn.addEventListener('click', getCurrentLocation);
