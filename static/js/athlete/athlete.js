// placing calendar in correct div
flatpickr("#selected-date");

//Side-nav Buttons to view past, current, and future sessions
const pastSessionsButton = document.querySelector("#past-sessions");
const todaysSessionsButton = document.querySelector("#todays-sessions");
const futureSessionsButton = document.querySelector("#future-sessions");
// Side-nav Buttons array
const sessionButtons = [pastSessionsButton, 
    todaysSessionsButton, 
    futureSessionsButton];



//Data-containers for past, present, and future pastSessionsButton
const pastSessionsContainer = document.querySelector("#past-sessions-container");
const todaysSessionsContainer = document.querySelector("#current-sessions-container");
const futureSessionsContainer = document.querySelector("#future-sessions-container");
//Session container array
const sessionContainers = [pastSessionsContainer,
    todaysSessionsContainer,
    futureSessionsContainer
];

//Side-nav button to add a session
const addSessionButton = document.querySelector("#add-session");
//Add session container and output rendered
const addSessionContainer = document.querySelector("#event-selection-container")
const sessionOutput = document.querySelector("#event-output")

//Side-nav button to log out
const logOutButton = document.getElementById("log-out");


//Log Out Function
if(logOutButton){
    logOutButton.addEventListener("click", () => {
        sessionContainers.forEach((container) => {
            container.style.display ="none";
        })
        addSessionContainer.style.display ="none";
        sessionOutput.style.display = "none";
        window.location.href = `/`;
    })
}else {
    console.warn("Log out button not found");
}

