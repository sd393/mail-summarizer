import PricingCard from '../components/PricingCard';
import '../components/PricingCard.css'; // We will create this new CSS file

function Pricing() {
  const standardFeatures = ["1 user", "Weekly Summaries"];
  const plusFeatures = ["1 user", "Weekly Summaries", "Custom Summary Style", "30-Day Free Trial"];
  const premiumFeatures = ["2+ users", "Custom Summary Frequency", "Custom Summary Style", "Reminders Enabled", "30-Day Free Trial"];

  return (
    <div>
        <div style = {{ 
            display: "flex",
            flexDirection: "column",
            textAlign: 'center', 
            paddingTop: '50px', 
            gap: "1.25rem",
            color: "black" 
        }}>
            <h1>Your week in review, straight to your inbox.</h1>
            <h3>Reliable. Cheap. Pensieve.</h3>
        </div>

        <div className="pricing-card-container">
            <PricingCard 
            planName="Standard"
            price="Free"
            features={standardFeatures}
            buttonText="Get Started"
            /> 
            <PricingCard 
            planName="Plus"
            price="$0.99 / month"
            features={plusFeatures}
            buttonText="Try Free"
            /> 
            <PricingCard 
            planName="Premium"
            price="$4.99 / month"
            features={premiumFeatures}
            buttonText="Try Free"
            /> 
        </div>
        
    </div>
  );
}

export default Pricing;
