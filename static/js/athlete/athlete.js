// Obtain form from HTML
const form = document.querySelector("#event-selection-form");

form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    //Construct object using FormData COnstructor
    const formData = new FormData(form);
    for (const entry of formData.entries()) {
        console.log(entry);
    }
    
    // Convert object to query string that will appear after end point
    const queryString = new URLSearchParams(formData).toString();
    console.log(queryString);

    // Fetch endpoint, handle response
    fetch(`/training_session_options/json?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
        switch(data.response){
            case "no events":
                alert(data.message);
                break;
            
            case "athlete unavailable":
                alert(data.message);
                break;
            
            case "coach unavailable":
                alert(data.message);
                break;
            
            case "events available":
                alert(1);
                break;
        }
    });
});