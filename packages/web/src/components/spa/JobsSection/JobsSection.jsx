import React from 'react';
import { NavBar } from '../Navigation/NavBar';
import axios from 'axios';
import { useState } from 'react';
import { Anchor, Props } from '../Navigation/NavFactory';
import { useEffect } from 'react';
import { url } from '../../../Global';
import { JobsCard } from './JobsCard';
import { Footer } from '../Footer/Footer';
import './jobs_section.css';

const anchorList = [
    new Anchor('About', '/#about'),
    new Anchor('Team', '/#team'),
    new Anchor('Jobs', '/jobs')
];

export const JobsSection = () => {
    const [jobs, setJobs] = useState([]);

    const getJobs = () => {
        axios({
            method: 'get',
            url: url + '/api/job'
        })
            .then((res) => {
                setJobs(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {});
    };
    useEffect(() => {
        getJobs();
    }, []);

    // eslint-disable-nextline no-extra-boolean-cost
    if (jobs) {
        return (
            <>
                <div className="jobs-page">
                    <NavBar props={new Props(anchorList, true)} />

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
                </div>
                <Footer
                    colour={'rgb(21, 76, 121)'}
                    iconcolor={'rgb(120, 120, 120)'}
                />
            </>
        );
    } else {
        return (
            <>
                <div className="jobs-page-error">
                    <NavBar props={new Props(anchorList, true)} />
                    <div>
                        <h1>No jobs available</h1>
                    </div>
                </div>
                <Footer />
            </>
        );
    }
};
