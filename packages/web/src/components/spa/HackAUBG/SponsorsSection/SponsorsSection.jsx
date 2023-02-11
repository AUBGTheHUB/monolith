import React from 'react';
import './sponsors_section.css';

export const Sponsors = () => {
    return (
        <div className="sponsors-main">
            <h1 className="sponsors-header">Sponsors</h1>
            <div className="sponsors-containers">
                <div className="platinum-container">
                    <h1>Platinum</h1> {/* Add here the background box design*/}
                    <div className="platinum-box">
                        {/* This will hold all the logos */}
                        {/* <img src="https://1000logos.net/wp-content/uploads/2017/09/Uber-logo.jpg" alt="Uber logo" /> */}
                    </div>
                </div>
                <div className="gold-container">
                    <h1>Gold</h1>
                    <div className="platinum-box">
                        {/* This will hold all the logos */}
                    </div>
                </div>
                <div className="custom-container">
                    <h1>Custom</h1>
                    <div className="platinum-box">
                        {/* This will hold all the logos */}
                    </div>
                </div>
                <div className="silver-container">
                    <h1>Silver</h1>
                    <div className="platinum-box">
                        {/* This will hold all the logos */}
                    </div>
                </div>
                <div className="bronze-container">
                    <h1>Bronze</h1>
                    <div className="platinum-box">
                        {/* This will hold all the logos */}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sponsors;
