import ListGroup from "../components/ListGroup";
import NavBar from "../components/NavBar";
import WelcomeTitle from "../components/WelcomeTitle";
import "../App.css";
function App() {
  const call = () => {
  }

  return (
    <div className = "App"> 
      <div className="main-title-container">
        <WelcomeTitle/>
        <div className = "email-form-container">
          <input
            type="email"
            placeholder="JohnDoe@gmail.com"
            className="email-input"
          />
          <button onClick={call} className = "submit-button">
            SUMMARIZE
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;


