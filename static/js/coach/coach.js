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

// Get the table body where data will be contained upon the form being  
// submitted
const addedEventsBody = document.querySelector("#added-events-body")

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
        }
    })
})