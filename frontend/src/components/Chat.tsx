import { useState } from "react";
import ChatQuery from "./ChatQuery";
import ChatHistory from "./ChatHistory";


export interface Message {
    id: number,
    content: string;
    role: string;
}

function Chat() {
    const [ history, setHistory] = useState<Message[]>([
        { id: 1, content: "What is today's weather in Sydney?", role: "user"},
        { id: 2, content: "Sydney today is blazing at 45 degree Celsius.", role: "system"}
    ]);

    const addMessage = (content: string, role: string) => {
        const newMessage: Message = {
            id: Date.now(),
            content,
            role
        };
        setHistory(prev => [ ...prev, newMessage ]);
    }

    return (
        <div className="chat-container">
            <ChatHistory history={history} />
            <ChatQuery onSend={addMessage} />
        </div>
    );
}

export default Chat;
