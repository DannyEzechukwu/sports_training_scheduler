let form = document.querySelector("#event-selection-form");

form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    const formData = {
        selectedDate: form.querySelector("#selected-date").value,
        selectedStartTime: form.querySelector("#selected-start-time").value,
        selectedCoach: form.querySelector("#selected-coach").value,
    };

    fetch("/training_session_options/json", {
        method: "GET", 
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.response == "no events") {
            alert(data.message);
        }
    });
});