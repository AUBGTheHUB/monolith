import React, { useContext } from 'react';
import { NavBar } from '../Navigation/NavBar';
import axios from 'axios';
import { useState, useEffect } from 'react';
import { Anchor, Props } from '../Navigation/NavFactory';
import { url } from '../../../Global';
import { JobsCard } from './JobsCard';
import { Footer } from '../Footer/Footer';
import './jobs_section.css';
import { FsContext } from '../../../feature_switches';

export const JobsSection = () => {
    // eslint-disable-next-line
    const [featureSwitches, _] = useContext(FsContext);

    const anchorList = [
        new Anchor('About', '/#about'),
        new Anchor('Team', '/#team', true, featureSwitches.team),
        new Anchor('Jobs', '/jobs', false, featureSwitches.jobs),
    ];
    const [jobs, setJobs] = useState();
    const [isFetching, setIsFetching] = useState(true);

    const getJobs = () => {
        axios({
            method: 'get',
            url: url + '/api/job',
        })
            .then(res => {
                setJobs(res.data.data.data);
                setTimeout(() => {
                    setIsFetching(false);
                }, 750);

                // force earlier download
                res.data.data.data.forEach(element => {
                    let img = new Image();
                    img.src = element.logo;
                });
            })
            // eslint-disable-next-line no-unused-vars
            .catch(err => {
                setIsFetching(false);
            });
    };
    useEffect(() => {
        getJobs();
        setIsFetching(true);
    }, []);

    const DisplayJobs = () => {
        if (jobs && !isFetching) {
            return (
                <div className="jobs-card-section">
                    <div className="jobs-section-body">
                        {jobs.map((job, index) => (
                            <JobsCard
                                key={index}
                                company={job['company']}
                                position={job['position']}
                                description={job['description']}
                                logo={job['logo']}
                                link={job['link']}
                            />
                        ))}
                    </div>
                </div>
            );
        } else if (isFetching) {
            return (
                <div className="jobs-loader">
                    <div className="lds-ellipsis">
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                    </div>
                </div>
            );
        }

        return (
            <div className="no-jobs-container">
                <img src="noJobsAvailable.png" className="no-jobs-image"></img>
            </div>
        );
    };
    return (
        <>
            <div className="jobs-page">
                <NavBar props={new Props(anchorList, true)} />
                {DisplayJobs()}
            </div>
            <Footer color={'rgb(21, 76, 121)'} iconColor={'rgb(255, 255, 255)'} iconBgColor={'rgb(120, 120, 120)'} />
        </>
    );
};
