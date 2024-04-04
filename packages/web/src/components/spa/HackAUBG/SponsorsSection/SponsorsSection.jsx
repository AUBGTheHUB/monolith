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
    const [mediaSponsors, setMediaSponsors] = useState({});
    const [isMediaLoaded, setIsMediaLoaded] = useState(false);
    const [isSponsprLoaded, setIsSponsorLoaded] = useState(false);

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
            setIsSponsorLoaded(true);
        });
        // eslint-disable-next-line no-unused-vars
        //removed catch to fix console error
    };

    const fetchMediaSponsors = () => {
        axios({
            method: 'get',
            url: url + '/api/partners',
        }).then(res => {
            const mediaSponsors = res.data.data.data;
            setMediaSponsors({ bronze: mediaSponsors });
            setIsMediaLoaded(true);
        });
    };

    useEffect(() => {
        if (featureSwitches.Sponsors) {
            fetchSponsors();
            fetchMediaSponsors();
        }
    }, [featureSwitches.Sponsors]);

    if (isMediaLoaded && isSponsprLoaded && featureSwitches.Sponsors) {
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
                    <SponsorsContainer sponsors={sponsor.platinum} category={'platinum'} isLoaded={isSponsprLoaded} />

                    <div className="sponsors-header-gold sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Gold</h1>
                    </div>
                    <SponsorsContainer sponsors={sponsor.gold} category={'gold'} isLoaded={isSponsprLoaded} />
                    <div className="sponsors-header-custom sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Custom</h1>
                    </div>

                    <SponsorsContainer sponsors={sponsor.custom} category={'custom'} isLoaded={isSponsprLoaded} />
                    <div className="sponsors-header-silver sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Silver</h1>
                    </div>
                    <img className="right-svg" src="FAQ-right.png" />

                    <SponsorsContainer sponsors={sponsor.silver} category={'silver'} isLoaded={isSponsprLoaded} />
                    {/* TODO: add hackathon partners to hackathon partners in admin panel */}
                    {/* !!!!!!! PUT IT IN A NEW COMPONENT !!!!!!!!! */}

                    <div className="sponsors-header-bronze sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Bronze</h1>
                    </div>
                    <SponsorsContainer sponsors={sponsor.bronze} category={'bronze'} isLoaded={isSponsprLoaded} />

                    <div className="sponsors-header-media sponsors-headers">
                        <h1 style={{ color: '#FFFFFF' }}>Media</h1>
                    </div>
                    <SponsorsContainer sponsors={mediaSponsors.bronze} category={'media'} isLoaded={isMediaLoaded} />
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
