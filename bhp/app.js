document.addEventListener('DOMContentLoaded', () => {
    fetchLocationNames();

    const form = document.getElementById('predictionForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await predictHomePrice();
    });
});

async function fetchLocationNames() {
    const response = await fetch('http://127.0.0.1:5000/get_location_names');
    const data = await response.json();
    
    const locationSelect = document.getElementById('location');
    data.locations.forEach(location => {
        const option = document.createElement('option');
        option.value = location;
        option.textContent = location;
        locationSelect.appendChild(option);
    });
}

async function predictHomePrice() {
    const total_sqft = document.getElementById('total_sqft').value;
    const location = document.getElementById('location').value;
    const bhk = document.getElementById('bhk').value;
    const bath = document.getElementById('bath').value;

    const response = await fetch('http://127.0.0.1:5000/predict_home_price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            total_sqft,
            location,
            bhk,
            bath,
        }),
    });

    const data = await response.json();
    
    const resultDiv = document.getElementById('result');
    if (response.ok) {
        resultDiv.textContent = `Estimated Price: ${data.estimated_price} lakh ₹`;
    } else {
        resultDiv.textContent = `Error: ${data.error}`;
    }
}
