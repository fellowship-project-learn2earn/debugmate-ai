import "./App.css";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import HowItWorks from "./components/HowItWorks";

function App() {
  return (
    <div className="app">
      <Navbar />

      <main>
        <Hero />
        <HowItWorks />
      </main>
    </div>
  );
}

export default App;