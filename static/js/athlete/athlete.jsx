function SideNav(){

    flatpickr("#selected-date");
    
    // State for athlete in session
    const[userName, setUserName] = React.useState("");
    // State for toggle symbol from Google
    const[isNavOpen, setIsNavOpen] = React.useState(true);

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

    // h1 page header
    const pageHeader = document.querySelector("#header")

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
                todaysSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addSessionContainer.style.display = "none";
                sessionsOutput.style.display = "none";
                pastSessionsContainer.style.display = "block";
                break;

        //Today's Sessions is clicked
            case "todays-sessions":
                pageHeader.innerText = "Today's Sessions";
                pastSessionsContainer.style.display = "none";
                futureSessionsContainer.style.display = "none";
                addSessionContainer.style.display = "none";
                sessionsOutput.style.display = "none";
                todaysSessionsContainer.style.display = "block";
                break;
        
        //Upcoming Sessions is clicked
                case "future-sessions":
                    pageHeader.innerText = "Upcoming Sessions";
                    pastSessionsContainer.style.display = "none";
                    todaysSessionsContainer.style.display = "none";
                    addSessionContainer.style.display = "none";
                    sessionsOutput.style.display = "none";
                    futureSessionsContainer.style.display = "block";
                    break;
        
        //Add Sessions is clicked
                case "add-sessions":
                    pageHeader.innerText = "Add Sessions";
                    sessionContainers.forEach((container) =>{
                        container.style.display = "none";
                    })
                    addSessionContainer.style.display = "flex";
                    break;
        }
      };
      
      document.querySelectorAll(".sidebar-options").forEach((button) => {
        button.addEventListener("click", handleClick);
      });


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
                    <li><button className="sidebar-options" id="past-sessions">Past Sessions</button></li>
                    <li><button className="sidebar-options" id="todays-sessions">Today's Sessions</button></li>
                    <li><button className="sidebar-options" id="future-sessions">Upcoming Sessions</button></li>
                    <li><button className="sidebar-options" id="add-sessions">Add Session</button></li>
                    <li><button className="sidebar-options" id="log-out">Log Out</button></li>
                </ul>
            </nav>
        </>
    );
};

ReactDOM.render(<SideNav/>, document.getElementById('side-nav'));