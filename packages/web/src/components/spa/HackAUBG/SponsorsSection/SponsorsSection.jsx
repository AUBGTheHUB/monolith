import React, { useState } from 'react';
import axios from 'axios';
import './sponsors_section.css';
import { url } from '../../../../Global';
import { useEffect } from 'react';
import SponsorsContainer from './SponsorContainer';

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

    useEffect(fetchSponsors, []);
    if (Object.keys(sponsorSections).length !== 0) {
        return (
            <div className="sponsors-main">
                <h1 className="sponsors-header">SPONSORS</h1>
                <div className="sponsors-containers">
                    <SponsorsContainer
                        sponsors={sponsorSections.platinum}
                        category={'platinum'}
                    />
                    <SponsorsContainer
                        sponsors={sponsorSections.gold}
                        category={'gold'}
                    />
                    <SponsorsContainer
                        sponsors={sponsorSections.custom}
                        category={'custom'}
                    />
                    <SponsorsContainer
                        sponsors={sponsorSections.silver}
                        category={'silver'}
                    />
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
