import React, { useState } from 'react';
import SponsorLogo from './SponsorLogo';
import axios from 'axios';
import './sponsors_section.css';
import { url } from '../../../../Global';

export const Sponsors = () => {
    // eslint-disable-next-line no-unused-vars
    const [sponsorSections, setSponsorSection] = useState({});

    const fetchSponsors = () => {
        let unfilteredSponsors;
        axios({
            method: 'get',
            url: url + '/api/sponsors'
        })
            .then((res) => {
                unfilteredSponsors = res.data.data.data;
                let tempSponsorSections = {
                    platinum: [],
                    gold: [],
                    bronze: [],
                    silver: [],
                    custom: []
                };

                unfilteredSponsors.forEach((x) => {
                    tempSponsorSections[x.category].push(x);
                });

                console.log(tempSponsorSections);

                setSponsorSection(tempSponsorSections);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {});
    };

    useState(fetchSponsors, []);

    const displaySponsors = (category) => {
        if (category in sponsorSections) {
            return sponsorSections[category].map((sponsor, index) => (
                <img src={sponsor.profilepicture} key={index} />
            ));
        }
    };

    return (
        <div className="sponsors-main">
            <h1 className="sponsors-header">SPONSORS</h1>
            <div className="sponsors-containers">
                <div className="platinum-container">
                    <h1>Platinum</h1> {/* Add here the background box design*/}
                </div>
                <div className="platinum-box">
                    <div className="logo-container">
                        {/* This will hold all the logos */}
                        <SponsorLogo
                            imageSrc="https://1000logos.net/wp-content/uploads/2017/09/Uber-logo.jpg"
                            altText="Uber logo"
                            onClick={() =>
                                (window.location.href = 'https://www.uber.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Chaos_logo.svg/1200px-Chaos_logo.svg.png"
                            altText="Chaos logo"
                            onClick={() =>
                                (window.location.href = 'https://www.chaos.com')
                            }
                        />

                        <SponsorLogo
                            imageSrc="https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Chaos_logo.svg/1200px-Chaos_logo.svg.png"
                            altText="Chaos logo"
                            onClick={() =>
                                (window.location.href = 'https://www.chaos.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://www.shapeblue.com/wp-content/uploads/2020/11/VMware-logo.jpg"
                            altText="vmware logo"
                            onClick={() =>
                                (window.location.href = 'https://vmware.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://1000logos.net/wp-content/uploads/2016/10/Bosch-Logo-1925.png"
                            altText="Bosch logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                    </div>
                </div>

                <div className="gold-container">
                    <h1>Gold</h1>
                </div>
                <div className="gold-box">
                    <div className="logo-container">
                        {displaySponsors('gold')}
                    </div>
                </div>

                <div className="custom-container">
                    <h1>Custom</h1>
                </div>
                <div className="custom-box">
                    <div className="logo-container">
                        {/* This will hold all the logos */}
                        <SponsorLogo
                            imageSrc="https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Chaos_logo.svg/1200px-Chaos_logo.svg.png"
                            altText="Chaos logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Chaos_logo.svg/1200px-Chaos_logo.svg.png"
                            altText="Chaos logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://1000logos.net/wp-content/uploads/2017/09/Uber-logo.jpg"
                            altText="Uber logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                    </div>
                </div>

                <div className="silver-container">
                    <h1>Silver</h1>
                </div>
                <div className="silver-box">
                    <div className="logo-container">
                        {/* This will hold all the logos */}
                        <SponsorLogo
                            imageSrc="https://www.shapeblue.com/wp-content/uploads/2020/11/VMware-logo.jpg"
                            altText="vmware logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://www.shapeblue.com/wp-content/uploads/2020/11/VMware-logo.jpg"
                            altText="vmware logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                    </div>
                </div>
                <div className="bronze-container">
                    <h1>Bronze</h1>
                </div>
                <div className="bronze-box">
                    <div className="logo-container">
                        {/* This will hold all the logos */}
                        <SponsorLogo
                            imageSrc="https://1000logos.net/wp-content/uploads/2016/10/Bosch-Logo-1925.png"
                            altText="Bosch logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://1000logos.net/wp-content/uploads/2016/10/Bosch-Logo-1925.png"
                            altText="Bosch logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                        <SponsorLogo
                            imageSrc="https://1000logos.net/wp-content/uploads/2016/10/Bosch-Logo-1925.png"
                            altText="Bosch logo"
                            onClick={() =>
                                (window.location.href = 'https://bosch.com')
                            }
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sponsors;
