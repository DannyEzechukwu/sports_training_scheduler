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

// Get the container to hide after form is submitted
const addEventsContainer = document.querySelector("#add-event-container")

// Get the container that needs to display once form is submitted
addEventForm.addEventListener("submit" , (event) => {
    event.preventDefault();
    const header = document.querySelector("#header");
    const subHeader = document.querySelector("#subheader");

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
                subHeader.innerText = "";
                addEventsContainer.style.display = "none";
                header.innerText= "Trainings You've Added"
                addedEventsContainer.style.display = "block";
            break;
        }
    })
})
// ***********************************************************************

// FEEDBACK SUBMISSION MODAL

// Get all cells that will be updated upon feedback being added
const tableDataUpdates = document.querySelectorAll(".update");

// Get all buttons where a coach needs to add feedback
const feedBackAdders = document.querySelectorAll(".feedback-adder");

// Get the modal and the button to closwe the modal
const modal = document.querySelector("[coach-feedback-modal]");
const modalCloser = document.querySelector("[modal-closer]");

// Get form that will be used to enter feedback: 
const feedbackForm = document.querySelector("#feedback-form");


// Open the Modal when an element of the feedBack Adders array is clicked
for(let i = 0; i < feedBackAdders.length; i++){
    
    feedBackAdders[i].addEventListener("click", (event) => {
        event.preventDefault();

        const tableDataUpdates = document.querySelectorAll(".update")

        // Get the hidden element in the feedback form and adjust
        // its value with the id of the feedBackAdder that was clicked
        // The value will be a string so need to convert to int on backend
        const hiddenFeedBack = document.querySelector("#feedback-id");
        hiddenFeedBack.value = feedBackAdders[i].id;

        // Open the modal
        modal.showModal();
    })

    feedbackForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(feedbackForm); 

        fetch("/add_feedback/json", {
            method: "POST", 
            body: formData
        })


    })
}

// Close Modal
modalCloser.addEventListener("click", () => {
    document.querySelector("#feedback-text").value="";
    modal.close();
})

// Close modal by clicking outside of it
modal.addEventListener("click", (evt) => {
    const dimensions = modal.getBoundingClientRect();
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
        document.querySelector("#feedback-text").value="";
        modal.close();
    }
});

// Prevent modal close when clicking inside the form fields
// Without this the event listener above will propogate down the DOM
// to the form in the modal
modal.querySelectorAll('div').forEach((element) => {
    element.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});


