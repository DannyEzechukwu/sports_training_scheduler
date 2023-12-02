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
    modal.querySelectorAll('div').forEach((element) => {
        element.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
}

// Function to handle submission of form for exisiting athletes and coaches
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
                console.log(data.response);
                alert("Username or password incorrect. Please try again");
            }else if(data.response == "valid coach"){
                //Go to correct endpoint if response is not"bad"
                window.location.href = `/coach/${data.id}/${data.fname}${data.lname}`;
            }
            else{
                window.location.href  = `/athlete/${data.id}/${data.fname}${data.lname}`
            }
        }) 
}
