import ChatQuery from "./ChatQuery";
import ChatHistory from "./ChatHistory";
import { useChat } from "../hooks/useChat";

export function Chat() {
    const { history, sendMessage } = useChat();

    return (
        <div className="chat-container">
            <ChatHistory history={history} />
            <ChatQuery onSend={(content) => sendMessage(content)} />
        </div>
    );
}

export default Chat;
