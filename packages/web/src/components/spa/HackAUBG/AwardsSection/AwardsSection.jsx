import React from 'react';
import './awards_section.css';

export const AwardsSection = () => {
    return (
        <div className="awards-section-container">
            <h1 className="awards-section-title">AWARDS</h1>
            <div className="awards-section-images-container">
                <div className="awards-pic-text">
                    <img
                        src="awardIconSilver.png"
                        alt="Silver award badge"
                        id="silver-img"
                    ></img>
                    <p className="award-money" id="silver-money-amt">
                        2000 BGN
                    </p>
                </div>
                <div className="awards-pic-text">
                    <img
                        src="awardIconGold.png"
                        alt="Gold award badge"
                        id="gold-img"
                    ></img>
                    <p className="award-money" id="gold-money-amt">
                        3000 BGN
                    </p>
                </div>
                <div className="awards-pic-text">
                    <img
                        src="awardIconBronze.png"
                        alt="Bronze award badge"
                        id="bronze-img"
                    ></img>
                    <p className="award-money" id="bronze-money-amt">
                        1000 BGN
                    </p>
                </div>
            </div>

            <div className="awards-section-info-text">
                <p id="awards-info-text">
                    And much more!
                    <br />
                    Take part in all of the games we have prepared!
                    <br />
                    All participants will recieve giftbags with swag from The
                    Hub and all HackAUBG 5.0 partners!
                </p>
            </div>
        </div>
    );
};
