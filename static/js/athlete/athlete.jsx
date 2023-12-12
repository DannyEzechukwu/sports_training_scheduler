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
        fetch("/athlete_info/json")
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

    //Add session container and output rendered
    const addSessionContainer = document.querySelector("#event-selection-container")
    const sessionsOutput = document.querySelector("#event-output")

    //Event handler for buttons side-nav panel
    const handleClick = (event) => {
        // Handle button clicks in side-nave based on ID
        switch (event.target.id) {    
        //Log Out is clicked
            case "log-out":
                sessionContainers.forEach((container) =>{
                    container.style.display = "none";
                })
                addSessionContainer.style.display = "none";
                sessionsOutput.style.display = "none";
                window.location.href = `/`;
                break;
        
        //Past Sessions is clicked
            case "past-sessions":
        //Handle today's sessions button click
                pageHeader.innerText = "Past Sessions";
                subHeader.style.display = "none";
                todaysSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addSessionContainer.style.display = "none";
                sessionsOutput.style.display = "none";
                pastSessionsContainer.style.display = "block";
                break;

        //Today's Sessions is clicked
            case "todays-sessions":
                pageHeader.innerText = "Today's Sessions";
                subHeader.style.display = "none";
                pastSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addSessionContainer.style.display = "none";
                sessionsOutput.style.display = "none";
                todaysSessionsContainer.style.display = "block";
                break;
        
        //Upcoming Sessions is clicked
                case "future-sessions":
                    pageHeader.innerText = "Upcoming Sessions";
                    subHeader.style.display = "none";
                    pastSessionsContainer.style.display = "none";
                    todaysSessionsContainer.style.display = "none";
                    addSessionContainer.style.display = "none";
                    sessionsOutput.style.display = "none";
                    futureSessionsContainer.style.display = "block";
                    break;
        
        //Add Sessions is clicked
                case "add-sessions":
                    sessionContainers.forEach((container) =>{
                        container.style.display = "none";
                    })
                    pageHeader.innerText = "Add Sessions";
                    subHeader.style.display = "block";
                    subHeader.innerHTML
                    addSessionContainer.style.display = "block";
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
                <ul> 
                    <li><button className="sidebar-options" id="past-sessions" onClick = {handleClick}>Past Sessions</button></li>
                    <li><button className="sidebar-options" id="todays-sessions" onClick = {handleClick}>Today's Sessions</button></li>
                    <li><button className="sidebar-options" id="future-sessions" onClick = {handleClick}>Upcoming Sessions</button></li>
                    <li><button className="sidebar-options" id="add-sessions" onClick = {handleClick}>Add Sessions</button></li>
                    <li><button className="sidebar-options" id="log-out" onClick = {handleClick}>Log Out</button></li>
                </ul>
            </nav>
        </>
    );
};

ReactDOM.render(<SideNav/>, document.querySelector('#side-nav'));
