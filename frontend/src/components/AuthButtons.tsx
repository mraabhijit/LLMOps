import { useState } from "react";
import useAuth from "../hooks/useAuth";
import { loginUser, registerUser } from "../api/auth";

function AuthButtons() {
    const {token, login, logout} = useAuth();
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const handleLogin = async () => {
        const token = await loginUser({email, password});
        if (!token) {
            console.log("Login failed");
            return;
        }
        login(token);
    };

    const handleRegister = async () => {
        await registerUser({email, password});
        const token = await loginUser({email, password});
        if (!token) return;
        login(token);
    };

    if (token) {
        return <button onClick={logout}>Logout</button>
    }

    return (
        <div>
            <input placeholder="user@user.com" onChange={(e) => setEmail(e.target.value)}/>
            <input type="password" placeholder="user@user" onChange={(e) => setPassword(e.target.value)}/>
            <button onClick={handleRegister}>Register</button>
            <button onClick={handleLogin}>Login</button>
        </div>
    );
}

export default AuthButtons;