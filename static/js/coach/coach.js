// ADD TRAINING FORM

// Update the end time when the start time is slected
const startTime = document.querySelector("#event-start-time");
const endTime =  document.querySelector("#event-end-time");

startTime.addEventListener("change", (event) => {
    switch (event.target.value){
        case "9:00 AM": 
            endTime.value = "10:00 AM";
            break;

        case "10:00 AM": 
            endTime.value = "11:00 AM"; 
            break;
        
        case "11:00 AM": 
            endTime.value = "12:00 PM";
            break;
        
        case "12:00 PM": 
            endTime.value = "1:00 PM";
            break;
            
        case "1:00 PM": 
            endTime.value = "2:00 PM";
            break;
        
        case "2:00 PM": 
            endTime.value = "3:00 PM";  
            break;
    }
})

// Handle the submission of form
const addEventForm = document.querySelector("#add-event-form");

// Get the container to be displayed and table body 
// data will contained in upon the form being submitted
const addedEventsContainer = document.querySelector("#added-events-container");
const addedEventsTableBody = document.querySelector("#added-events-body");
console.log(addedEventsTableBody);

// Get the container to hide after form is submitted
const addEventsContainer = document.querySelector("#add-event-container")

// Get the container that needs to display once form is submitted
addEventForm.addEventListener("submit" , (event) => {
    event.preventDefault();

    const formData = new FormData(addEventForm);

    fetch("/add_event/json", {
        method: "POST",
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        switch(data.response){
            case "event in the past": 
                alert(data.output);
                break;
            
            case "start date not after end date":
                alert(data.output);
                break;

            case "successful": 
                addedEventsTableBody.insertAdjacentHTML("beforeend", `
                <tr>
                    <td>${data.output.location}</td>
                    <td>${data.output.event}</td>
                    <td>${data.output.description}</td>
                    <td>${data.output.available}</td>
                </tr>`
                )
                addEventsContainer.style.display = "none";
                addedEventsContainer.style.display = "block";
            break;
        }
    })
})