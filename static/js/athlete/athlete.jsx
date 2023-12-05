function SideNav(){
    // State for athlete in session
    const[userName, setUserName] = React.useState("");
    // State for toggle symbol from Google
    const[isNavOpen, setIsNavOpen] = React.useState(false);

    React.useEffect(() => {
        fetch("/athlete_info/json")
          .then((response) => response.json())
          .then((data) => {
            setUserName(data.username)
        });
    }, [userName]);
    
    React.useEffect(() => {
        const handleResize = () => {
            if(window.innerWidth < 600 && isNavOpen){
                setIsNavOpen(false);
            }
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize",handleResize);
    }, [isNavOpen])

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
                    <li><button className="sidebar-options" id="future-sessions">Future Sessions</button></li>
                    <li><button className="sidebar-options" id="add-session">Add Session</button></li>
                    <li><button className="sidebar-options" id="log-out">Log Out</button></li>
                </ul>
            </nav>
        </>
    );
};

ReactDOM.render(<SideNav/>, document.getElementById('side-nav'));