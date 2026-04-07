import { useState } from "react";
import ChatQuery from "./ChatQuery";
import ChatHistory from "./ChatHistory";
import useAuth from "../hooks/useAuth";
import { getRecipe } from "../api/chat";


export interface Message {
    id: number,
    content: string;
    role: string;
}

export function Chat() {
    const { token } = useAuth();
    const [ history, setHistory] = useState<Message[]>([
        { id: Date.now(), content: "Welcome to Recipe Finder! Tell me the ingredients you have and I will help you with a quick and delicious recipe! ", role: "system"},
    ]);

    const addMessage = async (content: string, role: string) => {
        if (!content.trim()) return;
        
        // Add user message to history
        const newMessage: Message = {
            id: Date.now(),
            content,
            role
        };
        setHistory(prev => [ ...prev, newMessage ]);
        
        const res = await getRecipe({
            ingredients: content,
            allergies: [],
            language: "english",
        }, token!);
    
        // Add system response to history
        const response: Message = {
            id: Date.now(),
            content: res.recipe || res.error || "Sorry! Unable to fetch requested resource",
            role: "system",
        };
        setHistory(prev => [ ...prev, response ]);
    }

    return (
        <div className="chat-container">
            <ChatHistory history={history} />
            <ChatQuery onSend={addMessage} />
        </div>
    );
}

export default Chat;
