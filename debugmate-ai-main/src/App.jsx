import "./App.css";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import HowItWorks from "./components/HowItWorks";
import DebuggingWorkspace from "./components/DebuggingWorkspace";

function App() {
  return (
    <div className="app">
      <Navbar />

      <main>
        <Hero />
        <HowItWorks />
        <DebuggingWorkspace />
      </main>
    </div>
  );
}

export default App;