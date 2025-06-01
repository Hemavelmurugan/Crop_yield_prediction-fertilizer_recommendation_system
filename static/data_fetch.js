window.onload = function() {
    const fields = ["temperature", "humidity", "soil_ph", "soil_moisture", "rainfall", "sunlight_hours"];
    fields.forEach(field => {
        if (localStorage.getItem(field)) {
            document.getElementById(field).value = localStorage.getItem(field);
        }
    });
};
