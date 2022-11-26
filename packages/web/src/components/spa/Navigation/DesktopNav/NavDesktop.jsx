import React from "react";
import "./desktop_navbar.css";

export const NavDesktop = () => {
    return (
        <div className="navdesktop-container">
            <div className="navdesktop-logo">
                <img src="hublogo.png" className="navdesktop-logo-image" alt="The Hub AUBG" />
                <p>The HUB</p>
            </div>
            <div className="navdesktop-buttons">
                <a href= "#about">About</a>
                <a href= "#events">Events</a>
                <a href= "#articles">Articles</a>
                <a href= "#team">Team</a>
                <a href= "#jobs">Jobs</a>
                {/* <div>Link for the hackathon</div> */}
                <button className="button" type="button" onClick={() => {
                                }} >Hack AUBG</button>
            </div>
        </div>
        
    );
}