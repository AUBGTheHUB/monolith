import React, { useState } from 'react';
import axios from 'axios';
import './sponsors_section.css';
import { url } from '../../../../Global';
import { useEffect } from 'react';
import SponsorsContainer from './SponsorContainer';

const Sponsors = () => {
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

    useEffect(fetchSponsors, []);
    if (Object.keys(sponsorSections).length !== 0) {
        return (
            <div className="sponsors-main">
                <h1 className="sponsors-header">SPONSORS</h1>
                <div className="sponsors-containers">
                    <div className="sponsors-box-header-container-platinum">
                        <h1 style={{ color: '#FFFFFF' }}>Platinum</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsorSections.platinum}
                        category={'platinum'}
                    />
                    <div className="sponsors-box-header-container-gold">
                        <h1 style={{ color: '#FFFFFF' }}>Gold</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsorSections.gold}
                        category={'gold'}
                    />
                    <div className="sponsors-box-header-container-custom">
                        <h1 style={{ color: '#FFFFFF' }}>Custom</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsorSections.custom}
                        category={'custom'}
                    />
                    <div className="sponsors-box-header-container-silver">
                        <h1 style={{ color: '#FFFFFF' }}>Silver</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsorSections.silver}
                        category={'silver'}
                    />
                    <div className="sponsors-box-header-container-bronze">
                        <h1 style={{ color: '#FFFFFF' }}>Bronze</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsorSections.bronze}
                        category={'bronze'}
                    />
                </div>
            </div>
        );
    }
};

export default Sponsors;
