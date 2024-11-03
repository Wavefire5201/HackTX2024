document.getElementById('sendBtn').addEventListener('click', async () => {
    const input = document.getElementById('userInput').value;
    
    // Retrieve userID from storage or state, e.g. using localStorage
    const userID = localStorage.getItem('userID'); // Example, adjust as necessary
    
    // Retrieve Canvas API key from storage
    const canvasAPIKey = localStorage.getItem('canvasAPIKey'); // Example, adjust as necessary
    
    // Determine the course from context or user input; replace the following with actual logic
    const course = input; // Assuming input is course related. Adjust as necessary.

    // Now you can proceed to use these variables, e.g., call a function or send a request.
});


async function sendQuestion(question, course, userID) {
    const response = await fetch('https://your-api-endpoint.com/send_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, course, userID }),
    });
    const data = await response.json();
    return data.answer; // Assuming your API returns a response object
}
