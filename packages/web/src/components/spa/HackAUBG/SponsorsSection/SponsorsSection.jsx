import React from 'react';
import axios from 'axios';
import { url } from '../../../../Global';
import { useState, useEffect } from 'react';
import SponsorsContainer from './SponsorContainer';
import './sponsors_section.css';
import { FsContext } from '../../../../feature_switches';
import { useContext } from 'react';

const Sponsors = () => {
    // eslint-disable-next-line no-unused-vars
    const [sponsor, setSponsor] = useState({});
    // eslint-disable-next-line
    const [featureSwitches, _] = useContext(FsContext);

    const fetchSponsors = () => {
        let unfilteredSponsors;
        axios({
            method: 'get',
            url: url + '/api/sponsors',
        }).then(res => {
            unfilteredSponsors = res.data.data.data;
            let tempSponsor = {
                platinum: [],
                gold: [],
                bronze: [],
                silver: [],
                custom: [],
            };

            unfilteredSponsors.forEach(x => {
                tempSponsor[x.category].push(x);
            });

            setSponsor(tempSponsor);
        });
        // eslint-disable-next-line no-unused-vars
        //removed catch to fix console error
    };

    useEffect(fetchSponsors, []);
    if (Object.keys(sponsor).length !== 0 && featureSwitches.Sponsors) {
        return (
            <div className="sponsors-main">
                <h1 className="sponsors-header">SPONSORS</h1>
                <img
                    className="left-svg"
                    src="FAQ-left.png"
                    width="385"
                    height="619"
                    viewBox="0 0 385 619"
                    fill="none"
                />
                <div className="sponsors-containers">
                    <div className="sponsors-header-platinum sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Platinum</h1>
                    </div>
                    <SponsorsContainer sponsors={sponsor.platinum} category={'platinum'} />

                    <div className="sponsors-header-gold sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Gold</h1>
                    </div>
                    <SponsorsContainer sponsors={sponsor.gold} category={'gold'} />
                    <div className="sponsors-header-custom sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Custom</h1>
                    </div>

                    <SponsorsContainer sponsors={sponsor.custom} category={'custom'} />
                    <div className="sponsors-header-silver sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Silver</h1>
                    </div>
                    <img className="right-svg" src="FAQ-right.png" />

                    <SponsorsContainer sponsors={sponsor.silver} category={'silver'} />
                    {/* TODO: add hackathon partners to hackathon partners in admin panel */}
                    {/* !!!!!!! PUT IT IN A NEW COMPONENT !!!!!!!!! */}

                    <div className="sponsors-header-bronze sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Bronze Partners</h1>
                    </div>
                    <SponsorsContainer sponsors={sponsor.bronze} category={'bronze'} />
                </div>
            </div>
        );
    } else {
        return (
            <p className="sponsors_closed" id="registration">
                Sponsors coming soon!
            </p>
        );
    }
};

export default Sponsors;
