function getTableHeader() {
    return `<table border='1'><tr><td>Client Name</td><td>Previous Rating</td><td>Current Rating</td><td>Rating Change</td>
    <td>Number of Reviews</td><td>Reviews last week</td><td>Weeks since last review</td></tr>`;
}


var reviews_this_week_order = "descending";
var ratingChangeOrder = "descending";
var isClient = "False";
var currentTab = viewAll;


viewAll();


function isClientToggle() {
    if (isClient == "False") {
        isClient = "True";
        document.getElementById("client_filter_toggle").value = "Filtering Out prospective Clients"
    }
    else {
        isClient = "False"
        document.getElementById("client_filter_toggle").value = "Filtering Out Current Clients"
    }
    currentTab();
}

function isClientToggleRefresh() {
    if (isClient == "True") {
        document.getElementById("client_filter_toggle").value = "Filtering Out prospective Clients"
    }
    else {
        document.getElementById("client_filter_toggle").value = "Filtering Out Current Clients"
    }
}

function isClientToggleReset() {
    document.getElementById("client_filter_toggle").value = "Viewing All Clients"
}

function addClientToggleMask() {
    if (isClient == "True") {
        document.getElementById("client_filter_toggle").value = "Adding New Current Clients"
    }
    else {
        document.getElementById("client_filter_toggle").value = "Adding New Prospective Clients"
    }
}

/***************************************************************************
 * Creates a table of all the clients returned by ajax to all-businesses/ in 'results" div.
 */
function viewAll() {
    currentTab = viewAll;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            var table = "<h1></h1>" + `<table border='1'><tr><td>Client Name</td><td>Current Client</td><td>Previous Rating</td><td>Current Rating</td><td>Rating Change</td>
            <td>Number of Reviews</td><td>Reviews last week</td><td>Weeks since last review</td></tr>`;
            var ourButtonHalf = `<input class="button" type="button" onclick=viewBusinessDetails("` 

            obj.forEach(function (business) {
                if (business["is_client"] == true){
                    clientShape = "&#10004";
                }
                else {
                    clientShape = "";
                }
                table += "<tr><td>" + ourButtonHalf + business["place_id"] + "\") value=\"" + business["business_name"] + "\"</td>"
                    + "<td>" + clientShape + "</td>"
                    + "<td>" + business["previous_rating"] + "</td>"
                    + "<td>" + business["rating"] + "</td>"
                    + "<td>" + business["rating_delta"] + "</td>"
                    + "<td>" + business["total_reviews"] + "</td>"
                    + "<td>" + business["reviews_this_week"] + "</td>"
                    + "<td>" + Math.floor(business["days_since_last_review"] / 7) + "</td>"
                    + "</tr>";
            });

            table += "</table>";
            document.getElementById("results").innerHTML = table;
            document.getElementById("businessCompetitors").innerHTML = "";
            isClientToggleReset();
        }
    };
    xhttp.open("POST", "all-businesses/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`sort_by_is_client=True&csrfmiddlewaretoken=${csrftoken}`);
    clear();
}

/******************************************************************************
 * Creates a table of all the clients returned by ajax to review-velocity/ in "results" div.
 * They are sorted by the number of reviews.
 * It checks for client's status.
 * Reloading this will flip the sort.
 */
function filterReviewVelocity() {
    currentTab = filterReviewVelocity;
    isClientToggleRefresh();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            var table = "<h1>Review Velocity</h1>" + getTableHeader();
            var ourButtonHalf = `<input class="button" type="button" onclick=viewBusinessDetails("`

            obj.forEach(function (business) {
                table += "<tr><td>" + ourButtonHalf + business["place_id"] + "\") value=\"" + business["business_name"] + "\"</td>"
                    + "<td>" + business["previous_rating"] + "</td>"
                    + "<td>" + business["rating"] + "</td>"
                    + "<td>" + business["rating_delta"] + "</td>"
                    + "<td>" + business["total_reviews"] + "</td>"
                    + "<td>" + business["reviews_this_week"] + "</td>"
                    + "<td>" + Math.floor(business["days_since_last_review"] / 7) + "</td>"
                    + "</tr>";
            });

            table += "</table>";
            document.getElementById("results").innerHTML = table;
            document.getElementById("businessCompetitors").innerHTML = "";
        }
    };
    xhttp.open("POST", "review-velocity/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`order_by=${reviews_this_week_order}&is_client=${isClient}&csrfmiddlewaretoken=${csrftoken}`);
    clear();
    if (reviews_this_week_order == "descending") {
        reviews_this_week_order = "ascending";
    }
    else {
        reviews_this_week_order = "descending"
    }
}

/*****************************************************************
 * Creates a table of all the clients returned by ajax to negative-reviews/ in "results" div.
 * Positive rating changes are filterd out.
 * They are sorted by the rating changed.
 * It checks for client's status.
 * Reloading this function will flip the sort.
 */
function getBusinessScoreDropped() {
    currentTab = getBusinessScoreDropped;
    isClientToggleRefresh();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            var table = "<h1>Declining Reviews</h1>" + getTableHeader();
            var ourButtonHalf = `<input class="button" type="button" onclick=viewBusinessDetails("` 

            obj.forEach(function (business) {
                table += "<tr><td>" + ourButtonHalf + business["place_id"] + "\") value=\"" 
                    + business["business_name"] + "\"</td>"
                    + "<td>" + business["previous_rating"] + "</td>"
                    + "<td>" + business["rating"] + "</td>"
                    + "<td>" + business["rating_delta"] + "</td>"
                    + "<td>" + business["total_reviews"] + "</td>"
                    + "<td>" + business["reviews_this_week"] + "</td>"
                    + "<td>" + Math.floor(business["days_since_last_review"] / 7) + "</td>"
                    + "</tr>";
            });

            table += "</table>";
            document.getElementById("results").innerHTML = table;
            document.getElementById("businessCompetitors").innerHTML = "";
        }
    };
    xhttp.open("POST", "negative-reviews/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`rating_change_order=${ratingChangeOrder}&is_client=${isClient}&csrfmiddlewaretoken=${csrftoken}`);
    clear();
    if (ratingChangeOrder == "ascending") {
        ratingChangeOrder = "descending";
    }
    else {
        ratingChangeOrder = "ascending"
    }
}


/**************************************************************************
 * Removes a client from the system.
 */
function removeClient(place_id){
    var result = confirm("Are you sure you want to remove this business?"); 
    if (result == true) { 
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                alert("Client removed successfully!")
                clear();
                viewAll();
            }
        };
        xhttp.open("POST", "delete-client/", true);
        xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhttp.send(`place_id=${place_id}&csrfmiddlewaretoken=${csrftoken}`);
    } 
}

/**************************************************************************
 * Toggles a client from being a client and vise-versa.
 */
function toggleIsClient(place_id){
    var result = confirm("Are you sure you want to toggle this business?"); 
        if (result == true) { 
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                alert("Success!")
                currentTab();
            }
        };
        xhttp.open("POST", "toggle-client/", true);
        xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhttp.send(`place_id=${place_id}&csrfmiddlewaretoken=${csrftoken}`);
    }
}

/**************************************************************************
 * Creates a table of the selected client and its data.
 * Creates a table of all the clients that are competitors with the selected client.
 * Ajax request to get-business-competitors/.
 * Displays in "businessCompetitors" div.
 */
function viewBusinessCompetitors(place_id) {
    clear();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var client = JSON.parse(this.responseText);
            var table = "<h1>Client</h1>" + `<table border='1'><tr><td>Client Name</td><td>Current Client</td><td>Previous Rating</td><td>Current Rating</td><td>Rating Change</td>
            <td>Number of Reviews</td><td>Reviews last week</td><td>Weeks since last review</td></tr>`;
            client.forEach(function (business) {
                if (business["is_client"] == true){
                    clientShape = "&#10004";
                }
                else {
                    clientShape = "";
                }
                table += "<tr> <td>" + business["business_name"] + "</td>"
                    + "<td>" + clientShape + "</td>"    
                    + "<td>" + business["previous_rating"] + "</td>"
                    + "<td>" + business["rating"] + "</td>"
                    + "<td>" + business["rating_delta"] + "</td>"
                    + "<td>" + business["total_reviews"] + "</td>"
                    + "<td>" + business["reviews_this_week"] + "</td>"
                    + "<td>" + Math.floor(business["days_since_last_review"] / 7) + "</td>"
                    + "</tr>";
            });
            table += "</table>";
            
            document.getElementById("details").innerHTML = table;
            document.getElementById("buttons").innerHTML = `
                <input id="deleteClient" class="button" type="button" onclick="removeClient('${client[0].place_id}')" value="Delete Client">
                <input id="toggleClient" class="button" type="button" onclick="toggleIsClient('${client[0].place_id}')" value="Toggle Client">
            `;
            document.getElementById("addCompetitor").innerHTML
                = `<br/><input class="button" type="button" onclick="addCompetitor('${client[0].place_id}')" value="Add A Competitor">`;
            document.getElementById("removeCompetitor").innerHTML
                = `<br/><input class="button" type="button" onclick="removeCompetitor('${client[0].place_id}')" value="Remove Competitor">`;

            var table = "<h2>Competitors</h2>" + `<table border='1'><tr><td>Client Name</td><td>Current Client</td><td>Previous Rating</td><td>Current Rating</td><td>Rating Change</td>
            <td>Number of Reviews</td><td>Reviews last week</td><td>Weeks since last review</td></tr>`;
            if (client[0].competitor_1) {
                if (client[0].competitor_1["is_client"] == true){
                    clientShape = "&#10004";
                }
                else {
                    clientShape = "";
                }
                table += "<tr> <td>" + client[0].competitor_1["business_name"] + "</td>"
                    + "<td>" + clientShape + "</td>"  
                    + "<td>" + client[0].competitor_1["previous_rating"] + "</td>"
                    + "<td>" + client[0].competitor_1["rating"] + "</td>"
                    + "<td>" + client[0].competitor_1["rating_delta"] + "</td>"
                    + "<td>" + client[0].competitor_1["total_reviews"] + "</td>"
                    + "<td>" + client[0].competitor_1["reviews_this_week"] + "</td>"
                    + "<td>" + client[0].competitor_1["days_since_last_review"] % 7 + "</td>"
                    + "</tr>";
            }
            if (client[0].competitor_2) {
                if (client[1].competitor_1["is_client"] == true){
                    clientShape = "&#10004";
                }
                else {
                    clientShape = "";
                }
                table += "<tr> <td>" + client[0].competitor_2["business_name"] + "</td>"
                    + "<td>" + clientShape + "</td>"  
                    + "<td>" + client[0].competitor_2["previous_rating"] + "</td>"
                    + "<td>" + client[0].competitor_2["rating"] + "</td>"
                    + "<td>" + client[0].competitor_2["rating_delta"] + "</td>"
                    + "<td>" + client[0].competitor_2["total_reviews"] + "</td>"
                    + "<td>" + client[0].competitor_2["reviews_this_week"] + "</td>"
                    + "<td>" + client[0].competitor_2["days_since_last_review"] % 7 + "</td>"
                    + "</tr>";
            }
            if (client[0].competitor_3) {
                if (client[2].competitor_1["is_client"] == true){
                    clientShape = "&#10004";
                }
                else {
                    clientShape = "";
                }
                table += "<tr> <td>" + client[0].competitor_3["business_name"] + "</td>"
                    + "<td>" + clientShape + "</td>"  
                    + "<td>" + client[0].competitor_3["previous_rating"] + "</td>"
                    + "<td>" + client[0].competitor_3["rating"] + "</td>"
                    + "<td>" + client[0].competitor_3["rating_delta"] + "</td>"
                    + "<td>" + client[0].competitor_3["total_reviews"] + "</td>"
                    + "<td>" + client[0].competitor_3["reviews_this_week"] + "</td>"
                    + "<td>" + client[0].competitor_3["days_since_last_review"] % 7 + "</td>"
                    + "</tr>";
            }
            if (client[0].competitor_4) {
                if (client[3].competitor_1["is_client"] == true){
                    clientShape = "&#10004";
                }
                else {
                    clientShape = "";
                }
                table += "<tr> <td>" + client[0].competitor_4["business_name"] + "</td>"
                    + "<td>" + clientShape + "</td>"  
                    + "<td>" + client[0].competitor_4["previous_rating"] + "</td>"
                    + "<td>" + client[0].competitor_4["rating"] + "</td>"
                    + "<td>" + client[0].competitor_4["rating_delta"] + "</td>"
                    + "<td>" + client[0].competitor_4["total_reviews"] + "</td>"
                    + "<td>" + client[0].competitor_4["reviews_this_week"] + "</td>"
                    + "<td>" + client[0].competitor_4["days_since_last_review"] % 7 + "</td>"
                    + "</tr>";
            }
            if (client[0].competitor_5) {
                if (client[4].competitor_1["is_client"] == true){
                    clientShape = "&#10004";
                }
                else {
                    clientShape = "";
                }
                table += "<tr> <td>" + client[0].competitor_5["business_name"] + "</td>"
                    + "<td>" + clientShape + "</td>"  
                    + "<td>" + client[0].competitor_5["previous_rating"] + "</td>"
                    + "<td>" + client[0].competitor_5["rating"] + "</td>"
                    + "<td>" + client[0].competitor_5["rating_delta"] + "</td>"
                    + "<td>" + client[0].competitor_5["total_reviews"] + "</td>"
                    + "<td>" + client[0].competitor_5["reviews_this_week"] + "</td>"
                    + "<td>" + client[0].competitor_5["days_since_last_review"] % 7 + "</td>"
                    + "</tr>";
            }
            table += "</table>";
            document.getElementById("businessCompetitors").innerHTML = table;
        }
    };
    xhttp.open("POST", "get-business-competitors/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`place_id=${place_id}&csrfmiddlewaretoken=${csrftoken}`);
    clear();
}


function cancelCompetitorEdit(){
    clear();
    currentTab();
}


var competitor_ids = [];
function addCompetitor(place_id) {
    document.getElementById("addCompetitor").innerHTML = "";
    document.getElementById("removeCompetitor").innerHTML = "";
    document.getElementById("removeCompetitor").innerHTML
    = `<input id="cancel" class="button" type="button" onclick="cancelCompetitorEdit()" value="Cancel"></input>`;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            var select = document.getElementById("selectCompetitor");
            while (select.firstChild) {
                select.removeChild(select.firstChild);
            }
            var options = [];
            obj.forEach(function (each) {
                var el = document.createElement("option");
                el.textContent = each.business_name;
                el.value = each.business_name;
                bob = new Map([[each.business_name, each.place_id]]);
                competitor_ids.push(bob)
                select.appendChild(el);
            });
            document.getElementById("listCompetitor").style.display = "block";
            document.getElementById("editCompetitorSubmits").setAttribute("onclick", `addCompetitorSubmit('${place_id}')`);
        }
    };
    xhttp.open("POST", "get-not-competitors-on-client/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`place_id=${place_id}&csrfmiddlewaretoken=${csrftoken}`);
}
 

function removeCompetitor(place_id) {
    document.getElementById("removeCompetitor").innerHTML = "";
    document.getElementById("addCompetitor").innerHTML = "";
    document.getElementById("removeCompetitor").innerHTML
    = `<input id="cancel" class="button" type="button" onclick="cancelCompetitorEdit()" value="Cancel"></input>`;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            var select = document.getElementById("selectCompetitor");
            while (select.firstChild) {
                select.removeChild(select.firstChild);
            }
            var options = [];
            obj.forEach(function (each) {
                var el = document.createElement("option");
                el.textContent = each.business_name;
                el.value = each.business_name;
                bob = new Map([[each.business_name, each.place_id]]);
                competitor_ids.push(bob)
                select.appendChild(el);
            });
            document.getElementById("listCompetitor").style.display = "block";
            document.getElementById("editCompetitorSubmits").setAttribute("onclick", `removeCompetitorSubmit('${place_id}')`);
        }
    };
    xhttp.open("POST", "get-competitors-on-client/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`place_id=${place_id}&csrfmiddlewaretoken=${csrftoken}`);
}


function removeCompetitorSubmit(place_id) {
    competitorName = document.getElementById("selectCompetitor").value;
    var competitorID;
    competitor_ids.forEach(function (map) {
        if (map.get(competitorName)) {
            competitorID = map.get(competitorName);
        }
    });
    document.getElementById("addCompetitor").innerHTML = "";
    document.getElementById("removeCompetitor").innerHTML = "";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            viewBusinessCompetitors(place_id);
        }
        else if (this.readyState == 4) {
            document.getElementById("listCompetitor").innerHTML += "Unable to remove competitor.";
        }
    };
    xhttp.open("POST", "remove-competitor/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`place_id=${place_id}&competitor_place_id=${competitorID}&csrfmiddlewaretoken=${csrftoken}`);
}


function addCompetitorSubmit(place_id) {
    competitorName = document.getElementById("selectCompetitor").value;
    var competitorID;
    competitor_ids.forEach(function (map) {
        if (map.get(competitorName)) {
            competitorID = map.get(competitorName);
        }
    });
    document.getElementById("addCompetitor").innerHTML = "";
    document.getElementById("removeCompetitor").innerHTML = "";
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            viewBusinessCompetitors(place_id);
        }
        else if (this.readyState == 4) {
            document.getElementById("listCompetitor").innerHTML += "Unable to add competitor.";
        }
    };
    xhttp.open("POST", "add-a-new-competitor/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`place_id=${place_id}&competitor_place_id=${competitorID}&csrfmiddlewaretoken=${csrftoken}`);
}


function addClients() {
    currentTab = addClients;
    clear();
    addClientToggleMask();
    document.getElementById("results").innerHTML = `
        <div id="addClients">
            <h1>Add Clients</h1>
            <br/>
            <p>Add new clients by putting one placeid per line or separated by a space.</p>
            <p>Duplicate entries will be ignored.</p>
            <br/>
            <textarea id="new_place_ids" cols="50" rows="5"></textarea>
            <input class="button" type="button" onclick="submitClients()" value="Add Clients">
        </div>
    `
}


function submitClients() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            if (obj.status == "OK"){
                if (isClient == true){
                    alert("Added clients successfully!")
                }
                else{
                    alert("Added prospective clients successfully!")
                }
                viewAll();
            }
            else {
                alert(obj.error, "All prior entries added successfully.")
            }
        }
    };
    xhttp.open("POST", "sumbmitNewPlaceIDs/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`new_place_ids=${document.getElementById("new_place_ids").value}&is_client=${isClient}&csrfmiddlewaretoken=${csrftoken}`);
}


function clear() {
    competitor_ids = [];
    document.getElementById("businessCompetitors").innerHTML = "";
    document.getElementById("results").innerHTML = "";
    document.getElementById("details").innerHTML = "";
    document.getElementById("buttons").innerHTML = "";
    document.getElementById("addCompetitor").innerHTML = "";
    document.getElementById("removeCompetitor").innerHTML = "";
    document.getElementById("listCompetitor").style.display = "none";
}


function viewBusinessDetails(place_id) {
    viewBusinessCompetitors(place_id);
}



/*****************************************************************
 * I don't think this is in use??
 */
function displayCompetitors() {
    currentTab = displayCompetitors;
    isClientToggleRefresh();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            var table = "<h1>Competitors</h1>" + getTableHeader();
            var ourButtonHalf = `<input class="button" type="button" onclick=viewBusinessCompetitors("`

            obj.forEach(function (business) {
                table += "<tr><td>" + ourButtonHalf + business["place_id"] + "\") value=\"" 
                    + business["business_name"] + "\"</td>"
                    + "<td>" + business["previous_rating"] + "</td>"
                    + "<td>" + business["rating"] + "</td>"
                    + "<td>" + business["rating_delta"] + "</td>"
                    + "<td>" + business["total_reviews"] + "</td>"
                    + "<td>" + business["reviews_this_week"] + "</td>"
                    + "<td>" + Math.floor(business["days_since_last_review"] / 7) + "</td>"
                    + "</tr>";
            });

            table += "</table>";
            document.getElementById("results").innerHTML = table;
        }
    };
    xhttp.open("POST", "all-businesses-with-competitors/", true);
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhttp.send(`is_client=${isClient}&csrfmiddlewaretoken=${csrftoken}`);
    clear();
}
