//Obtain form from HTML within the eventsOutputContainer
const form = document.querySelector("#date-selection-form");
//Obtain the container div in HTML
const eventsOutputContainer = document.querySelector("#events-output");
//Get element in HTML that will contain the output of available events
const eventsOutputBody = document.querySelector("#events-output-body");

form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    //Make eventsOutputContainer visible on the page
    eventsOutputContainer.style.display = "block"

    //Construct object using FormData Constructor
    const formData = new FormData(form);
    for (const entry of formData.entries()) {
        console.log(entry);
    }
    
    // Convert object to query string that will appear after end point
    // for successful GET request
    const queryString = new URLSearchParams(formData).toString();
    console.log(queryString);

    // Fetch endpoint, handle response
    fetch(`/training_session_options/json?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
        switch(data.response){
            case "unsuccessful":
                alert(data.output);
                break;
            
            case "successful":
                let htmlContent ="";
                data.output.forEach((session)=>{
                   htmlContent += `
                   <tr>
                        <td><input type="checkbox" name="event-schedule${session.id}" value="${session.id}"></td>
                        <td>${session.month}/${session.date}/${session.year}</td>
                        <td>${session.duration}</td>
                        <td>${session.location}</td>
                        <td>${session.event_name}</td>
                        <td>${session.description}</td>
                        <td>${session.available_coaches}</td>
                    </tr>
                   `;
                }) 
                eventsOutputBody.innerHTML = htmlContent;
                break;
        }
    });
});

const eventsOutputForm = document.querySelector("#events-output-form");
const maxAllowedCheckboxes = 1;

eventsOutputForm.addEventListener("submit", (evt) => {
    evt.preventDefault();

    const checkedCheckBoxes = document.querySelectorAll('input[type="checkbox"]:checked');

    if (checkedCheckBoxes.length > maxAllowedCheckboxes) {
        // If more than the allowed checkboxes are checked, uncheck the last checkbox
        checkedCheckBoxes[1].checked = false;
        alert(`You can only select up to ${maxAllowedCheckboxes} options.`);
    }
});