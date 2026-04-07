import type {Message} from './Chat';
import ReactMarkdown from 'react-markdown';

interface ChatHistoryProps {
    history: Message[];
}

function ChatHistory({ history }: ChatHistoryProps) {
    return (
        <div className="chat-history-container">
            {history.map((m) => (
                <div key={m.id} className={`message ${m.role === "user" ? "user-message" : "system-message"}`}>
                    <ReactMarkdown>{m.content}</ReactMarkdown>
                </div>
            ))}
        </div>
    );
}

export default ChatHistory;