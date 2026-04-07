import './App.css'
// import Header from './components/Header'
import Chat from './components/Chat'
import useAuth from './hooks/useAuth'
import AuthButtons from './components/AuthButtons';
import { AuthProvider } from './context/AuthContext';

function AppContent() {
  const {token} = useAuth();

  return (
    <div>
      <AuthButtons />
      {token && <Chat />}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </ AuthProvider>
  )
}

export default App
