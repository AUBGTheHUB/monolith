import React from 'react';
import './awards_section.css';

export const AwardsSection = () => {
    return (
        <div className="awards-section-hack-aubg-container">
            <h1 className="awards-section-title">AWARDS</h1>
            <div className="awards-section-images-container">
                <div className="awards-pic-text">
                    <img
                        src="awardIcon.png"
                        alt="Award Silver"
                        id="silver-img"
                    ></img>
                    <p id="award-money">2000 BGN</p>
                </div>
                <div className="awards-pic-text">
                    <img
                        src="awardIcon.png"
                        alt="Award Gold"
                        id="gold-img"
                    ></img>
                    <p id="award-money">3000 BGN</p>
                </div>
                <div className="awards-pic-text">
                    <img
                        src="awardIcon.png"
                        alt="Award Bronze"
                        id="bronze-img"
                    ></img>
                    <p id="award-money">1000 BGN</p>
                </div>
            </div>
            <div className="awards-section-info-text">
                <p id="awards-info-text">
                    And much more!<br></br>
                    Take part in all of the games we have prepared!<br></br>
                    All participants will recieve giftbags with swag from The
                    Hub and all HackAUBG 5.0 partners!
                </p>
            </div>
        </div>
    );
};
