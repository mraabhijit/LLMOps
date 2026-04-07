import { BASE_URL } from "./auth";

interface RecipeRequest {
    ingredients: string;
    allergies: string[];
    language: string;
}

export async function getRecipeBatch(request: RecipeRequest, token: string) {
    const res = await fetch(`${BASE_URL}/recipe/batch/text`, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify(request),
        }
    );
    const data = await res.json();
    return data;
}

export async function getRecipe(request: RecipeRequest, token: string) {
    const res = await fetch(`${BASE_URL}/recipe/stream/text`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(request),
    });

    if (!res.ok) {
        throw new Error(`Failed to fetch: ${res.statusText}`);
    }
    return res.body;
}

