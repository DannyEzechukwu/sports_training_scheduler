// Obtain form from HTML within the eventsOutputContainer
const form = document.querySelector("#date-selection-form");
// Modal output for available sessions based on dates
const athleteSessionsModal = document.querySelector("[athlete-choices-modal]");
// Get element in HTML that will contain the output of available events
const eventsOutputBody = document.querySelector("#events-output-body");
// Button to close modal
const athleteSessionsModalCloser = document.querySelector("[modal-closer]")

form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    //Make athleteSessionsModal appear
    athleteSessionsModal.showModal();
    
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
            case "start date not after end date":
                alert(data.output);
                break;

            case "no events avaialble":
                alert(data.output);
                break;
            
            case "successful":
                let htmlContent ="";
                data.output.forEach((session)=>{
                
                // Create radio buttons for each coach in the available_coaches list
                const coachRadioButtons = session.available_coaches.map((coach, index) => `
                <div>
                    <input type="radio" name="event-coach-${session.id}" value="${coach}" id="coach-${session.id}-${index}">
                    <label for="coach-${session.id}-${index}">Coach ${coach}</label>
                </div>
            `).join("");
                   htmlContent += `
                   <tr>
                        <td><input type="checkbox" name="event-schedule-${session.id}" value="${session.id}"></td>
                        <td>${session.month}/${session.date}/${session.year}</td>
                        <td>${session.duration}</td>
                        <td>${session.location}</td>
                        <td>${session.event_name}</td>
                        <td>${session.description}</td>
                        <td id="coaches">${coachRadioButtons}</td>
                    </tr>
                   `;
                }) 
                eventsOutputBody.innerHTML = htmlContent;
                break;
        }
    });
});

//Close the modal that appears with all the events
athleteSessionsModalCloser.addEventListener("click", () => {
    athleteSessionsModal.close();
})

// Close athleteSessionsModal by clicking outside of it
athleteSessionsModal.addEventListener("click", (evt) => {
    const dimensions = athleteSessionsModal.getBoundingClientRect();
    if (
        //Event occurs outside the left edge of open modal
        evt.clientX < dimensions.left ||
        //Event occurs outside the right edge of open modal
        evt.clientX > dimensions.right ||
        //Event occurs beyond the top edge of open modal
        evt.clientY > dimensions.top ||
        //Event occurs below the bottom edge of open modal
        evt.clientY < dimensions.bottom
    ) { 
        athleteSessionsModal.close();
    }
});

// Prevent modal close when clicking inside the form fields
// Without this the event listener above will propogate down the DOM
// to the form in the modal
athleteSessionsModal.querySelectorAll('div').forEach((element) => {
    element.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});

//Minimize the amount of sessions an athlete can schedule at one time
const eventsOutputForm = document.querySelector("#events-output-form");
const maxAllowedCheckboxes = 3;

eventsOutputForm.addEventListener("change", (evt) => {
    evt.preventDefault();

    const checkedCheckBoxes = document.querySelectorAll('input[type="checkbox"]:checked');

    if (checkedCheckBoxes.length > maxAllowedCheckboxes) {
        // If more than the allowed checkboxes are checked, uncheck the last checkbox
        checkedCheckBoxes[3].checked = false;
        alert(`You can only select a maximum ${maxAllowedCheckboxes} sessions at a time.`);
    }
});

// Submit the entire form to the corresponding route on teh server 
// to handle the submission
eventsOutputForm.addEventListener("submit", (evt) =>{
    evt.preventDefault();

    // Check if at least 1 checkbox is selected
    const checkedCheckBoxes = document.querySelectorAll('input[type="checkbox"]:checked');
    if (checkedCheckBoxes.length == 0){
        alert("You must select at least 1 session");
    }

    const formData = new FormData(eventsOutputForm);

    fetch("/training_session_selections/json", {
        method: "POST",
        body: formData,
    })
    .then((response) => response.json())
    .then((data) =>{
        console.log(data.response)
    })
})
