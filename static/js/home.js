// Homepage Script

//Login buttons
const coachButton = document.querySelector("#coaches");
const newCoachButton = document.querySelector("#new-coaches")
const athleteButton = document.querySelector("#athletes");
const newAthleteButton = document.querySelector("#new-athletes");
//Login buttons array
const buttons = [coachButton, newCoachButton, athleteButton, newAthleteButton];

//Modals
const coachModal =  document.querySelector("[coach-modal]");
const newCoachModal = document.querySelector("[new-coach-modal]");
const athleteModal =  document.querySelector("[athlete-modal]");
const newAthleteModal =  document.querySelector("[new-athlete-modal]");
//Modals Array
const modals = [coachModal, newCoachModal, athleteModal, newAthleteModal];

//Modal Forms
const coachForm = document.querySelector("#coach-form");
const newCoachForm = document.querySelector("#new-coach-form");
const athleteForm = document.querySelector("#athlete-form");
const newAthleteForm = document.querySelector("#new-athlete-form");
//Modal Form Arrays
const modalForms = [coachForm, newCoachForm, athleteForm, newAthleteForm];

//Close Modal Buttons
const closeCoachModal = document.querySelector("[coach-modal-closer]");
const closeNewCoachModal = document.querySelector("[new-coach-modal-closer]");
const closeAthleteModal = document.querySelector("[athlete-modal-closer]");
const closeNewAthleteModal = document.querySelector("[new-athlete-modal-closer]");
//Closers Array
const closers = [closeCoachModal, closeNewCoachModal, closeAthleteModal, closeNewAthleteModal];

// Loop to open the the corresponding modal with the correct button
for(let i in buttons){
    buttons[i].addEventListener("click", () => {
        modals[i].showModal();
    })
}

// Loop to close corresponding modal with correct &times button;
for(let i in closers){
    closers[i].addEventListener("click", () => {
        clearFormData(modalForms[i].id);
        modals[i].close();
    })
}

//Loop to close any modal by clicking outside of it
for (let i = 0; i <= modals.length; i++) {
    modals[i].addEventListener("click", (evt) => {
        const dimensions = modals[i].getBoundingClientRect();
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
            clearFormData(modalForms[i].id);
            modals[i].close();
        }
    });
    // Prevent modal close when clicking inside the form fields
    // Without this the event listener above will propogate down the DOM
    // to the form in the modal
    modals[i].querySelectorAll('div').forEach((element) => {
        element.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
}

//Function to clear form data when modal is closed
//Parameter is the id value of the form
function clearFormData(formID) {
    form = document.getElementById(formID);
    // Iterate through form elements
    for (let i = 0; i < form.elements.length; i++) {
        // Check if the element is an input field
        if (form.elements[i].type !== 'button' && form.elements[i].type !== 'submit') {
            // Reset the value
            form.elements[i].value = '';
        }
    }
}

//Function to handle submission of form for exisiting athletes and coaches
function handleCurrentAccountFormSubmission(event, formID){
    // Prevent default behavior
    event.preventDefault()
    // Get the form we are working with by using the formID 
    // string parameter passed into the function
    const form = document.getElementById(formID);
    // Use FormData constructor to create a new object of key value pairs from form
    const formData = new FormData(form);

    // Fetch the endpoint the form is submitted to
    fetch(form.action, {
        // Specify the request type
        method: "POST",
        // Establish the body
        body: formData,
    })
        .then((response) => response.json())
        .then((data) =>{
            if (data.response == "invalid"){
                alert("Username or password incorrect. Please try again");
            }else if(data.response == "valid coach"){
                //Go to correct endpoint if coach response is valid
                window.location.href = `/coach/${data.id}/${data.fname}${data.lname}`;
            }
            else{
                //Go to correct endpoint if athlete response is valid
                window.location.href = `/athlete/${data.id}/${data.fname}${data.lname}`
            }
        }) 
}

//Function to handle submission of form for new athletes and coaches 
function handleNewAccountFormSubmission(event, formID){
    //Prevent default behavior
    event.preventDefault()
    // Get the form we are working with by using the formID 
    // string parameter passed into the function
    const form = document.getElementById(formID);
    // Use FormData constructor to create a new object of key value pairs from form
    const formData = new FormData(form);

    // Fetch the endpoint the form is submitted to
    fetch(form.action, {
        // Specify the request type
        method: "POST",
        // Establish the body
        body: formData,
    })
        .then((response) => response.json())
        .then((data) =>{
            if (data.response == "invalid username"){
                alert(data.message);
            }else if(data.response == "invalid email"){
                alert(data.message)
            }else if(data.response == "valid coach"){
                //Go to correct coach endpoint if coach response is valid
                window.location.href = `/coach/${data.id}/${data.fname}${data.lname}`;
            }
            else{
                // Got to correct athlete endpoint if athlete response is valid
                window.location.href  =`/athlete/${data.id}/${data.fname}${data.lname}`
            }
        }) 
}