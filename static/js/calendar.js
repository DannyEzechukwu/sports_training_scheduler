// Keep track of month (-2 = Nov, -1 = Dec, 0 - Jan, 1 = Feb, 2 = March)
let nav = 0;

// Indicator for day that is selected
let clicked = null;

//Access the calendar div in DOM
const calendar = document.querySelector("#calendar");

// Establish days of the week in an array
const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 'Friday', "Saturday"]

function loadCalendar(){
    // new date object 
    const dt = new Date();
    // console.log(dt);

    //Initially sets month at the top of the calendar to the current month
    // Updates the month and the year at the top of the calendar 
    // as a user moves forward and backward using global nav variable
    if (nav !== 0){
        dt.setMonth(new Date().getMonth() + nav);
    }

    const day = dt.getDate();
    const month = dt.getMonth();
    const year = dt.getFullYear();

    // Provides a date object for the first day of the current month
    const firstDayofMonth = new Date(year, month, 1);

    // Final paremeter in Date object is final day of the previous month
    // i.e. month = 0 + 1 (February), 0 indicates January 31
    // This lets us know the number of squares to render on the screen
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Turn firstDayof Month object into readable string
    const dateString = firstDayofMonth.toLocaleDateString("en-us", {
        weekday: "long", 
        year: "numeric",
        month : "long", 
        day : "numeric",
    });
    
    // Obtain the index of the weekday produced from dateString in 
    // weekdays array to establish number of days before first day of month
    const paddingDays = weekdays.indexOf(dateString.split(", ")[0]);

    //Includes the month and year at the top of calendar
    document.querySelector("#monthDisplay").innerText = 
        `${dt.toLocaleDateString("en-us", {month: "long"})} ${year}`;

    
    // Clear current calendar before new calendar is rendered is renedered
    calendar.innerHTML = "";


    // Loop through total number of squares that will be rendered on screen
    // between padding days and days in number of days in month
    for (let i = 1; i <= paddingDays + daysInMonth; i ++){
        //Create div for each iteration
        const daySquare= document.createElement('div');
        //Include a class called "day" for each div that is created
        daySquare.classList.add("day");
        //Include an id of "month-day(date - paddingDays)" for each div that is created
        daySquare.id = `month-day${i - paddingDays}`;
        
        // if i is an actual day in the month
        if(i > paddingDays){
            //Date showed in square
            daySquare.innerText = i - paddingDays;

            daySquare.addEventListener("click", () => console.log("click"));

        } else{
            daySquare.classList.add("padding");
        }

        //Append each daySquare div to the calendar container
        calendar.appendChild(daySquare);

    }
};

function initButtons(){
    document.querySelector("#nextButton").addEventListener("click", () =>{
        nav++;
        loadCalendar();
    })

    document.querySelector("#backButton").addEventListener("click", () =>{
        nav--;
        loadCalendar()
    })
}

initButtons();
loadCalendar();

