import { useState } from "react";

interface ChatQueryProps {
    onSend: (content: string, role: string) => void;
}

function ChatQuery( {onSend} : ChatQueryProps ) {
    const [ text, setText ] = useState<string>("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (text.trim() === "") return;

        onSend(text, "user");
        setText("");
    };

    return (
        <form onSubmit={handleSubmit} className="query-box">
            <input 
                type="text"
                value={text}
                placeholder="Type a message..."
                onChange={(e) => setText(e.target.value)}
            />
            <button type="submit">Send</button>
        </form>
    );
}

export default ChatQuery;