import React from 'react';
import axios from 'axios';
import { url } from '../../../../Global';
import { useState, useEffect } from 'react';
import SponsorsContainer from './SponsorContainer';
import './sponsors_section.css';

const Sponsors = () => {
    // eslint-disable-next-line no-unused-vars
    const [sponsor, setSponsor] = useState({});

    const fetchSponsors = () => {
        let unfilteredSponsors;
        axios({
            method: 'get',
            url: url + '/api/sponsors'
        })
            .then((res) => {
                unfilteredSponsors = res.data.data.data;
                let tempSponsor = {
                    platinum: [],
                    gold: [],
                    bronze: [],
                    silver: [],
                    custom: []
                };

                unfilteredSponsors.forEach((x) => {
                    tempSponsor[x.category].push(x);
                });

                setSponsor(tempSponsor);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {});
    };

    useEffect(fetchSponsors, []);
    if (Object.keys(sponsor).length !== 0) {
        return (
            <div className="sponsors-main">
                <h1 className="sponsors-header">SPONSORS</h1>
                <div className="sponsors-containers">
                    <div className="sponsors-header-platinum sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Platinum</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsor.platinum}
                        category={'platinum'}
                    />
                    <div className="sponsors-header-gold sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Gold</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsor.gold}
                        category={'gold'}
                    />
                    <div className="sponsors-header-custom sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Custom</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsor.custom}
                        category={'custom'}
                    />
                    <div className="sponsors-header-silver sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Silver</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsor.silver}
                        category={'silver'}
                    />
                    <div className="sponsors-header-bronze sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Media Sponsors</h1>
                    </div>
                    <SponsorsContainer
                        sponsors={sponsor.bronze}
                        category={'bronze'}
                    />
                </div>
            </div>
        );
    }
};

export default Sponsors;
