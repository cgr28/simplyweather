// favorite.js
// logic for the favorite button

let fav = document.querySelector("#favorite");
// console.log('id' + "{{ data.id }}" + "=" + "{{ data.id }}");

// if cookie exists already exist start as "unfavorite" else start as favorite
if (document.cookie.indexOf('id' + "{{ data.id }}" + "=" + "{{ data.id }}") > -1) {
    fav.innerHTML = "Un-favorite";
} else {
    fav.innerHTML = "Favorite";
}

function eraseCookie(name) {   
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;" // changes cookie exp date to make it expire
}

function favorite() {
    let fav = document.querySelector("#favorite");
    // favorite city
    if (fav.innerHTML === "Favorite") {
        let curr = new Date();
        let id = "{{ data.id }}" // city id
        curr.setMonth( curr.getMonth() + 1);
        document.cookie = "id" + id + "=" + id + "; expires=" + curr.toUTCString() + "; path=/"; // create cookie
        fav.innerHTML = "Un-favorite"
        // console.log("success");
    } else { //unfavorite city
        let curr = new Date();
        let id = "{{ data.id }}"; // city id
        eraseCookie('id' + "{{ data.id }}" + "=" + "{{ data.id }}");
        fav.innerHTML = "Favorite";
        // console.log("removed");
    }
}

document.querySelector("#favorite").addEventListener("click", favorite);