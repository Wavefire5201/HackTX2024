async function checkUser(canvasAPIKey) {
    const response = await fetch('https://your-api-endpoint.com/check_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ apiKey: canvasAPIKey }),
    });
    const data = await response.json();
    return data; // Returns userID if exists, otherwise null
}

async function createUser(canvasAPIKey) {
    const response = await fetch('https://your-api-endpoint.com/create_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ apiKey: canvasAPIKey }),
    });
    return await response.json(); // Returns new user data
}

async function handleUser(canvasAPIKey) {
    let user = await checkUser(canvasAPIKey);
    if (!user) {
        user = await createUser(canvasAPIKey);
    }
    return user; // Returns user object with userID and other details
}
