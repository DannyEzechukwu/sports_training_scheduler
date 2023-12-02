// Home page modals

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

//Close Modal Buttons
const closeCoachModal = document.querySelector("[coach-modal-closer]");
const closeNewCoachModal = document.querySelector("[new-coach-modal-closer]");
const closeAthleteModal = document.querySelector("[athlete-modal-closer]");
const closeNewAthleteModal = document.querySelector("[new-athlete-modal-closer]");
//Closers Array
const closers = [closeCoachModal, closeNewAthleteModal, closeAthleteModal, closeNewAthleteModal];

// Loop to open the the corresponding modal with the correct button
for(let i in buttons){
    buttons[i].addEventListener("click", () => {
        modals[i].showModal();
    })
}

function handleFormSubmission(formID){
    const form = document.getElementById(formID);
    const formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) =>{
            if (data.response == "ok"){
                console.log(data.response);
            }else{
                alert("Email or password incorrect. Please try again");
                form.preventDefault();
            }
        })
    
}

function redirectToPreviousPage() {
    const previousPageURL = document.referrer;
    
    // Check if there is a previous page URL
    if (previousPageURL) {
        // Redirect to the previous page
        window.location.href = previousPageURL;
    } else {
        // If no previous page URL, redirect to a default page
        window.location.href = '/';
    }
}

// Loop to close corresponding modal with correct &times button;
for(let i in closers){
    closers[i].addEventListener("click", () => {
        modals[i].close();
    })
}

//Loop to close any modal by clicking outside of it
for (let modal of modals) {
    modal.addEventListener("click", (evt) => {
        const dimensions = modal.getBoundingClientRect();
        if (
            evt.clientX < dimensions.left ||
            evt.clientX > dimensions.right ||
            evt.clientY > dimensions.top ||
            evt.clientY < dimensions.bottom
        ) {
            modal.close();
        }
    });
    // Prevent modal close when clicking inside the form fields
    // Without this the event listener above will propogate down the DOM
    // to the form in the modal
    modal.querySelectorAll('form input, form button, form select, form textarea').forEach((element) => {
        element.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
}

