// Home page modals

//Coaches login modal
const coachButton = document.querySelector("#coaches");
const coachModal =  document.querySelector("[coach-modal]");
const closeCoachModal = document.querySelector("[coach-modal-closer]");

coachButton.addEventListener("click", () => {
    coachModal.showModal();
})

closeCoachModal.addEventListener("click", () => {
    coachModal.close();
})

//Athletes login modal
const athleteButton = document.querySelector("#athletes");
const athleteModal =  document.querySelector("[athlete-modal]");
const closeAthleteModal = document.querySelector("[athlete-modal-closer]");

athleteButton.addEventListener("click", () => {
    athleteModal.showModal();
})

closeAthleteModal.addEventListener("click", () => {
    athleteModal.close();
})

//New Athlete login modal
const newAthleteButton = document.querySelector("#new-athletes");
const newAthleteModal =  document.querySelector("[new-athlete-modal]");
const closeNewAthleteModal = document.querySelector("[new-athlete-modal-closer]");

newAthleteButton.addEventListener("click", () => {
    newAthleteModal.showModal();
})

closeNewAthleteModal.addEventListener("click", () => {
    newAthleteModal.close();
})

//Closing any modal by clicking outside of it
const homeModalArray = [coachModal, athleteModal, newAthleteModal];

for(let modal of homeModalArray){
    modal.addEventListener("click", (evt) => {
        const dimensions = modal.getBoundingClientRect();
        if(
            evt.clientX < dimensions.left ||
            evt.clientX > dimensions.right ||
            evt.clientY > dimensions.top ||
            evt.clientY < dimensions.bottom
        ){
            modal.close();
        }
    })
}