import type {Message} from './Chat';

interface ChatHistoryProps {
    history: Message[];
}

function ChatHistory({ history }: ChatHistoryProps) {
    return (
        <div className="chat-history-container">
            {history.map((m) => (
                (m.role === "user")
                ? <p key={m.id} className="message user-message">{m.content}</p>
                : <p key={m.id} className="message system-message">{m.content}</p>
            ))}
        </div>
    );
}

export default ChatHistory;