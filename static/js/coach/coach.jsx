function SideNav(){
    //Header at the top of the page
    const pageHeader = document.querySelector("#header");
    const subHeader = document.querySelector("#subheader");

    //State for athlete in session
    const[userName, setUserName] = React.useState("");
    //State for toggle symbol from Google
    const[isNavOpen, setIsNavOpen] = React.useState(true);

    // Update the state of userName by fetching the endpoint from the server
    React.useEffect(() => {
        fetch("/coach_info/json")
            .then((response) => response.json())
            .then((data) => {
            setUserName(data.username)
        });
    }, []);

    //Ability for side-nav panel to fit to screen
    React.useEffect(() => {
        const handleResize = () => {
            if(window.innerWidth < 600 && isNavOpen){
                setIsNavOpen(false);
            }
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize",handleResize);
    }, [isNavOpen])

    //Data-containers for past, present, and future pastSessionsButton
    const pastSessionsContainer = document.querySelector("#past-sessions-container");
    const todaysSessionsContainer = document.querySelector("#current-sessions-container");
    const futureSessionsContainer = document.querySelector("#future-sessions-container");
    //Session container array
    const sessionContainers = [pastSessionsContainer,
    todaysSessionsContainer,
    futureSessionsContainer
    ];

    //Add event container and form
    const addEventContainer = document.querySelector("#add-event-container");

    // Added event container
    const addedEventContainer = document.querySelector("#added-events-container");

    // Function to clear add-event-form when a coach
    // navigates to different view
    // Original plan was to pass the form id into the function and then
    // obtain the elementby passing it into querySelector
    function clearAddEventForm() {
        // Get the form element
        const addEventForm = document.querySelector("#add-event-form");
    
        // Iterate through form inputs and clear their values
        for (let i = 0; i < addEventForm.elements.length; i++) {
            const element = addEventForm.elements[i];
            // Check if the element is an input field or textarea
            if (element.type !== "button" && element.type !== "submit") {
                // Clear current input value
                element.value = "";
            }
        }
    }

    //Event handler for buttons side-nav panel
    const handleClick = (event) => {
        // Handle button clicks in side-nave based on ID
        switch (event.target.id) {    
        //Log Out is clicked
            case "log-out":
                sessionContainers.forEach((container) =>{
                    container.style.display = "none";
                })
                addEventContainer.style.display = "none";
                addedEventContainer.style.display = "none";
                clearAddEventForm();
                window.location.href = `/`;
                break;
        
        //Past Sessions is clicked
            case "past-sessions":
                pageHeader.innerText = "Past Sessions";
                subHeader.innerText = "";
                todaysSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addEventContainer.style.display = "none";
                addedEventContainer.style.display = "none";
                clearAddEventForm();
                pastSessionsContainer.style.display = "block";
                break;

        //Today's Sessions is clicked
            case "todays-sessions":
                pageHeader.innerText = "Today's Sessions";
                subHeader.innerText = "";
                pastSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addEventContainer.style.display = "none";
                addedEventContainer.style.display = "none";
                clearAddEventForm();
                todaysSessionsContainer.style.display = "block";
                break;
        
        //Upcoming Sessions is clicked
                case "future-sessions":
                    pageHeader.innerText = "Upcoming Sessions";
                    subHeader.innerText = "";
                    pastSessionsContainer.style.display = "none";
                    todaysSessionsContainer.style.display = "none";
                    addEventContainer.style.display = "none";
                    addedEventContainer.style.display = "none";
                    clearAddEventForm();
                    futureSessionsContainer.style.display = "block";
                    break;
        
        //Add Event is clicked
                case "add-event":
                    sessionContainers.forEach((container) =>{
                        container.style.display = "none";
                    })
                    addedEventContainer.style.display = "none";
                    pageHeader.innerText = "Add A Training Event";
                    subHeader.innerText = "Trainings must be scheduled for 1 hour";
                    addEventContainer.style.display = "block";
                    break;
                    
        //Events Added is clicked
                case "events-added":
                    sessionContainers.forEach((container) =>{
                        container.style.display = "none";
                    })
                    addEventContainer.style.display = "none";
                    pageHeader.innerText = "Trainings You've Added";
                    subHeader.innerText = "";
                    clearAddEventForm();
                    addedEventContainer.style.display = "block";
                    break;
                    
        }
      };

    return (
        <>
            {/* Toggle between toggle_on and toggle_off for symbol on click */}
            <button className="sidebar-toggle" onClick={() => setIsNavOpen(!isNavOpen) }>
                {/* Ternary operator between open and close */}
                <span className="material-symbols-outlined">
                    {isNavOpen? "toggle_on":"toggle_off"}
                </span>
            </button>
            
            <nav className = {`nav ${isNavOpen ? "nav-open" : "nav-closed"}`}>
                <div className="logo">GAINZ</div>
                <div className="baby-logo">Let's work {userName}!</div>
                <ul> 
                    <li><button className="sidebar-options" id="past-sessions" onClick = {handleClick}>Past Sessions</button></li>
                    <li><button className="sidebar-options" id="todays-sessions" onClick = {handleClick}>Today's Sessions</button></li>
                    <li><button className="sidebar-options" id="future-sessions" onClick = {handleClick}>Upcoming Sessions</button></li>
                    <li><button className="sidebar-options" id="add-event" onClick = {handleClick}>Add Training Event</button></li>
                    <li><button className="sidebar-options" id="events-added" onClick = {handleClick}>Training Events</button></li>
                    <li><button className="sidebar-options" id="log-out" onClick = {handleClick}>Log Out</button></li>
                </ul>
            </nav>
        </>
    );
};

ReactDOM.render(<SideNav/>, document.querySelector('#side-nav'));
