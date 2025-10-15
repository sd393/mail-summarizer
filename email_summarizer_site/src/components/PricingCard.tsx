import "./PricingCard.css";

interface PricingCardProps {
  planName: string;
  price: string;
  features: string[];
  buttonText: string;
  isFeatured?: boolean; 
}

function PricingCard({ planName, price, features, buttonText, isFeatured }: PricingCardProps) {
  const cardClassName = "pricing-card"; /*isFeatured ? "pricing-card featured" : "pricing-card";*/

return (
    <div className={cardClassName}>
      {/*{isFeatured && <div className="best-value-banner">Best Value</div>}*/}
      
      <div>
        <h3 style={{ paddingTop: '1.5rem', paddingLeft: '1.5rem'}}>{planName}</h3>
        <p className="price">{price}</p>
      </div>
      
      <button className="buy-button">{buttonText}</button> 
      
      
    <ul className="features-list">
        {features.map((feature, index) => (
        <li key={index}>{feature}</li>
        ))}
    </ul> 
      
    </div>
  );
}

export default PricingCard;