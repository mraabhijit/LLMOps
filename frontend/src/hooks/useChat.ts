import { useState } from "react";
import useAuth from "../hooks/useAuth";
import { getRecipe } from "../api/chat";


export interface Message {
    id: number,
    content: string;
    role: string;
}

export const useChat = () => {
    const { token } = useAuth();
    const [ history, setHistory] = useState<Message[]>([
        { id: Date.now(), content: "Welcome to Recipe Finder!", role: "system"},
        { id: Date.now() + 1, content: "Tell me the ingredients you have and I will help you with a quick and delicious recipe!", role: "system"},
    ]);

    const sendMessage = async (content: string) => {
        if (!content.trim() || !token) return;
        
        // Add user message to history
        const userMsg: Message = {
            id: Date.now(),
            content,
            role: "user",
        };
        setHistory(prev => [...prev, userMsg]);
        
        // Placeholder for system response
        const systemId = Date.now() + 1;
        const messagePlaceholder: Message = {
            id: systemId,
            content: "",
            role: "system",
        }
        setHistory(prev => [...prev, messagePlaceholder]);

        const response = await getRecipe({
            ingredients: content,
            allergies: [],
            language: "english",
        }, token);
        
        if (!response) {
            console.error("The response body is null.");
            return;
        }
        
        const reader = response.getReader();
        const decoder = new TextDecoder();
        let accumulatedText = "";

        while (true) {
            const {done, value} = await reader.read();
            if (done) break;

            const rawChunk = decoder.decode(value);
            const lines = rawChunk.split("\n");

            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    const text = line.replace("data: ", "");
                    accumulatedText += text;

                    setHistory(prev => prev.map(msg =>
                        msg.id === systemId ? { ...msg, content: accumulatedText } : msg
                    ))
                }
            }
        }
    };

    return { history, sendMessage };
};
