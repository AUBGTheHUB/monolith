import React from 'react';
import './sponsors_section.css';

export const Sponsors = () => {
    return (
        <div className="sponsors-main">
            <h1 className="sponsors-header">Sponsors</h1>
            <div className="sponsors-containers">
                <div className="platinum-container">
                    <h1>Platinum</h1> {/* Add here the background box design*/}
                </div>
                <div className="platinum-box">
                    {/* This will hold all the logos */}
                    <img
                        src="https://1000logos.net/wp-content/uploads/2017/09/Uber-logo.jpg"
                        alt="Uber logo"
                    />
                    <img
                        src="https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Chaos_logo.svg/1200px-Chaos_logo.svg.png"
                        alt="Chaos logo"
                    />
                    <img
                        src="https://www.shapeblue.com/wp-content/uploads/2020/11/VMware-logo.jpg"
                        alt="vmware logo"
                    />
                    <img
                        src="https://1000logos.net/wp-content/uploads/2016/10/Bosch-Logo-1925.png"
                        alt="Bosch logo"
                    />
                </div>
                <div className="gold-container">
                    <h1>Gold</h1>
                </div>
                <div className="gold-box">
                    {/* This will hold all the logos */}
                    <img
                        src="https://1000logos.net/wp-content/uploads/2017/09/Uber-logo.jpg"
                        alt="Uber logo"
                    />
                </div>
                <div className="custom-container">
                    <h1>Custom</h1>
                </div>
                <div className="custom-box">
                    {/* This will hold all the logos */}
                    <img
                        src="https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Chaos_logo.svg/1200px-Chaos_logo.svg.png"
                        alt="Chaos logo"
                    />
                </div>
                <div className="silver-container">
                    <h1>Silver</h1>
                </div>
                <div className="silver-box">
                    {/* This will hold all the logos */}
                    <img
                        src="https://www.shapeblue.com/wp-content/uploads/2020/11/VMware-logo.jpg"
                        alt="vmware logo"
                    />
                </div>
                <div className="bronze-container">
                    <h1>Bronze</h1>
                </div>
                <div className="bronze-box">
                    {/* This will hold all the logos */}
                    <img
                        src="https://1000logos.net/wp-content/uploads/2016/10/Bosch-Logo-1925.png"
                        alt="Bosch logo"
                    />
                </div>
            </div>
        </div>
    );
};

export default Sponsors;
