function SideNav(){
    //Header at the top of the page
    const pageHeader = document.querySelector("#header");

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

    //Add event container
    const addEventContainer = document.querySelector("#add-event-container");

    // Added event container
    const addedEventContainer = document.querySelector("#added-events-container");

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
                window.location.href = `/`;
                break;
        
        //Past Sessions is clicked
            case "past-sessions":
                pageHeader.innerText = "Past Sessions";
                todaysSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addEventContainer.style.display = "none";
                addedEventContainer.style.display = "none";
                pastSessionsContainer.style.display = "block";
                break;

        //Today's Sessions is clicked
            case "todays-sessions":
                pageHeader.innerText = "Today's Sessions";
                pastSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addEventContainer.style.display = "none";
                addedEventContainer.style.display = "none";
                todaysSessionsContainer.style.display = "block";
                break;
        
        //Upcoming Sessions is clicked
                case "future-sessions":
                    pageHeader.innerText = "Upcoming Sessions";
                    pastSessionsContainer.style.display = "none";
                    todaysSessionsContainer.style.display = "none";
                    addEventContainer.style.display = "none";
                    addedEventContainer.style.display = "none";
                    futureSessionsContainer.style.display = "block";
                    break;
        
        //Add Event is clicked
                case "add-event":
                    sessionContainers.forEach((container) =>{
                        container.style.display = "none";
                    })
                    addedEventContainer.style.display = "none";
                    pageHeader.innerText = "Add An Event";
                    addEventContainer.style.display = "block";
                    break;
        //Events Added is clicked
                case "events-added":
                    sessionContainers.forEach((container) =>{
                        container.style.display = "none";
                    })
                    addEventContainer.style.display = "none";
                    pageHeader.innerText = "Events You've Added";
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
                <div className="baby-logo">Let's work {userName}</div>
                <ul> 
                    <li><button className="sidebar-options" id="past-sessions" onClick = {handleClick}>Past Sessions</button></li>
                    <li><button className="sidebar-options" id="todays-sessions" onClick = {handleClick}>Today's Sessions</button></li>
                    <li><button className="sidebar-options" id="future-sessions" onClick = {handleClick}>Upcoming Sessions</button></li>
                    <li><button className="sidebar-options" id="add-event" onClick = {handleClick}>Add Event</button></li>
                    <li><button className="sidebar-options" id="events-added" onClick = {handleClick}>Events Added</button></li>
                    <li><button className="sidebar-options" id="log-out" onClick = {handleClick}>Log Out</button></li>
                </ul>
            </nav>
        </>
    );
};

ReactDOM.render(<SideNav/>, document.querySelector('#side-nav'));
