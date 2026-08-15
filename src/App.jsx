import "./App.css";
import Navbar from "./components/Navbar";

function App() {
  return (
    <div className="app">
      <Navbar />

      <main>
        <h1>DebugMate</h1>
        <p>Your AI-powered debugging tutor.</p>
      </main>
    </div>
  );
}

export default App;