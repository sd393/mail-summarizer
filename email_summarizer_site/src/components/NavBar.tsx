import React from 'react';
import './NavBar.css';

const NavBar = () => {
  return (

<nav className="navbar">
  <div className="navbar-left">
    <ul className="nav-links">
      <li>
        <a href="/" className="logo">
        Mail Summarizer
        </a>
      </li>
      <li>
        <a href="/products">Products</a>
      </li>
      <li>
        <a href="/pricing">Pricing</a>
      </li>
    </ul>
  </div>
  <div className="navbar-right">
    <ul className="nav-links">
      <li>
        <a href="/about">About</a>
      </li>
      <li>
        <a href="/contact">Contact</a>
      </li>
      <li>
        <a href="/start" className="get-started">
        </a>
      </li>
      <li>
        <a href="/account" className="user-icon">
        <i className="fas fa-user"></i>
        </a>
      </li>
    </ul>
    
  </div>
</nav>
);
};

export default NavBar;