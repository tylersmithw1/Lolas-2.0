import React from 'react';
import './Hero.css';
import heroImage from '../assets/food-background.jpg';


function Hero() {
    return (
      <div className="hero">
        <img src={heroImage} alt="Hero" className="hero-image" />
      </div>
    );
  }
  
  export default Hero;