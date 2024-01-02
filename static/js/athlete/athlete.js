// FRONTEND OUTPUT

// Obtain form from HTML within the eventsOutputContainer
const dateForm = document.querySelector("#date-selection-form");
// Get element in HTML that will contain the output of available events
const eventsOutputBody = document.querySelector("#events-output-body");

// Declare checkedCheckBoxes array
// Use let keyword for the ability to overwrite the array later in the code
let checkedCheckBoxes = [];

// EventListener for when athlete selects dates to choose 
// events between
dateForm.addEventListener("submit", (evt) => {
    evt.preventDefault();
    
    //Construct object using FormData Constructor
    const formData = new FormData(dateForm);
    
    // Convert object to query string that will appear after end point
    // for successful GET request
    const queryString = new URLSearchParams(formData).toString();
    // console.log(queryString);

    // Fetch endpoint, handle response
    fetch(`/training_session_options/json?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
        switch(data.response){
            // Dates not in chronilogical order
            case "event in the past":
                alert(data.output);
                break;

            case "start date not after end date":
                alert(data.output);
                break;
            
            // No events within selected dates
            case "no events available":
                alert(data.output);
                break;
            
            // Events returned to front end successfully
            case "successful":
                //Make athleteSessionsModal appear
                athleteSessionsModal.showModal();
                
                let htmlContent ="";
                data.output.forEach((event)=>{
                
                // Create radio buttons for each coach in array returned from 
                // the available_coaches key for each element of array we have 
                // named "event"
                const coachRadioButtons = event.available_coaches.map((coach, index) => `
                <div>
                    <input 
                        type="radio" 
                        name="event-coach-${event.id}" 
                        value="${coach}" 
                        id="coach-${event.id}-${index}" 
                        required 
                        disabled
                    >
                    <label for="coach-${event.id}-${index}">Coach ${coach}</label>
                </div>
            `).join("");
                // Create rows for each element in array we named "event"
                htmlContent += `
                    <tr>
                        <td>
                            <input 
                                type="checkbox" 
                                id="event-schedule-${event.id}" 
                                name="event-schedule-${event.id}" 
                                value="${event.id}"
                            >
                        </td>
                        <td>${event.month}/${event.date}/${event.year}</td>
                        <td>${event.duration}</td>
                        <td>${event.location}</td>
                        <td>${event.event_name}</td>
                        <td>${event.description}</td>
                        <td id="coaches">${coachRadioButtons}</td>
                    </tr>
                `;
                }) 
                eventsOutputBody.innerHTML = htmlContent;
                
                // Get all checkBoxes that appear in the form
                // to create condition to enable radio buttons
                const checkBoxes = eventsOutputBody.querySelectorAll('input[type="checkbox"]');
                checkBoxes.forEach((checkBox) => {
                    // Change event listener as a checkbox is selected
                    //  or deselected
                    checkBox.addEventListener("change", () => {
                        // Find the parent row of the checkbox
                        const row = checkBox.closest('tr');
                        // Get radio buttons in this row
                        const radioButtons = row.querySelectorAll('input[type="radio"]');
                        // Enable or disable radio buttons based on checkbox state
                        radioButtons.forEach((radioButton) => {
                            // radio button is disabled in initial state 
                            // checkbox is unchecked in it's initisal state
                            // true = not false
                            radioButton.disabled = !checkBox.checked;
                        })
                        // Update the checkedCheckBoxes array to be the NodeList
                        // returned fronm the querySelector of checked checkboxes
                        checkedCheckBoxes = document.querySelectorAll('input[type="checkbox"]:checked');
                    })
                })
                
                // Get the form that holds the table returned for evemnts
                const eventsOutputForm = document.querySelector("#events-output-form");
                // Extablish the maximum amount of checkboxes that can be selected
                // at one time
                const maxAllowedCheckboxes = 3;

                // Change event listener to monitor number of checked check boxes
                // as they are selected to ensure there are not more than 3
                // at a time
                eventsOutputForm.addEventListener("change", (evt) => {
                    evt.preventDefault();

                    // Get the Array object from the checkBoxes NodeList
                    const checkBoxesArray = Array.from(checkBoxes);
                    // Get the Array object from the checkedCheckBoxes NodeList
                    const checkedCheckBoxesArray = Array.from(checkedCheckBoxes);

                    // Condition for if maxAllowedCheckboxes have been selected
                    if (checkedCheckBoxesArray.length == maxAllowedCheckboxes) {
                        // Loop through each possible checkBox with forEach
                        checkBoxesArray.forEach((checkBox) =>{
                            // Condition for if a checkBox has not been selected
                            // !Array.includes = "does not include/is not in"
                            if (!checkedCheckBoxesArray.includes(checkBox)){
                                // Disable checkBox
                                checkBox.disabled = true;
                            }
                        })
                    } else{
                        checkBoxesArray.forEach((checkBox) =>{
                            if (!checkedCheckBoxesArray.includes(checkBox)){
                                // Enable checkBox
                                checkBox.disabled = false;
                            }
                        })
                    }

                });
                break;
        }
    });
});
// ************************************************************************

// ADD SESSIONS MODAL

// Modal output for available sessions based on dates
const athleteSessionsModal = document.querySelector("[athlete-choices-modal]");
// Button to close modal
const athleteSessionsModalCloser = document.querySelector("[modal-closer]");

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
// ********************************************************************************

// ADD SESSIONS MODAL FORM SUBMISSION

// Get form for event outputs
const eventsOutputForm = document.querySelector("#events-output-form");

// Submit the entire form to the corresponding route on the server 
// to handle the submission
eventsOutputForm.addEventListener("submit", (evt) =>{
    evt.preventDefault();

    // Get start date and end date entered to clear form once submitted 
    const startDate = document.querySelector("#selected-start-date");
    const endDate = document.querySelector("#selected-end-date");

    // Condition for if no selections are made
    const checkedCheckBoxes = document.querySelectorAll('input[type="checkbox"]:checked');
    if (checkedCheckBoxes.length == 0){
        alert("You must select at least 1 session.");
    }

    // Establish the object that will be passed in the body
    const formData = new FormData(eventsOutputForm);

    fetch("/training_session_selections/json", {
        method: "POST",
        body: formData,
    })
    .then((response) => response.json())
    .then((data) =>{
        
        alert(data.response);
        startDate.value = "";
        endDate.value = "";
        athleteSessionsModal.close();
        location.reload();
    })
})
