import { Routes, Route } from 'react-router-dom'; // Import these
import NavBar from "./components/NavBar";
import Home from './pages/Home'; // Import your new pages
import Pricing from './pages/Pricing';
import "./App.css";

function App() {
  return (
    <div className="App">
      <NavBar /> {/* This will appear on every page */}
      
      {/* This is where the page content will be swapped out */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/pricing" element={<Pricing />} />
      </Routes>
    </div>
  );
}

export default App;