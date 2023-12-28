// ADD TRAINING FORM SUBMISSION

// Update the end time when the start time is slected
const startTime = document.querySelector("#event-start-time");
const endTime =  document.querySelector("#event-end-time");

startTime.addEventListener("change", (event) => {
    switch (event.target.value){
        case "9:00 AM": 
            endTime.value = "10:00 AM";
            break;

        case "10:00 AM": 
            endTime.value = "11:00 AM"; 
            break;
        
        case "11:00 AM": 
            endTime.value = "12:00 PM";
            break;
        
        case "12:00 PM": 
            endTime.value = "1:00 PM";
            break;
            
        case "1:00 PM": 
            endTime.value = "2:00 PM";
            break;
        
        case "2:00 PM": 
            endTime.value = "3:00 PM";  
            break;
    }
})