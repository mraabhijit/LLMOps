export const BASE_URL: string = "http://localhost:8000"

export interface User {
    email: string;
    password: string;
}

export async function registerUser(user: User) {
    await fetch(`${BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user),
    });
}

export async function loginUser(user: User) {
    const res = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user),
    });

    const data = await res.json();
    return data.access_token;
}
