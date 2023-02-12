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
    const [jobs, setJobs] = useState([{}]);

    const getJobs = () => {
        axios({
            method: 'get',
            url: url + '/api/job'
        })
            .then((res) => {
                setJobs(res.data.data.data);
                console.log(res.data.data.data);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    useEffect(() => {
        getJobs();
    }, []);
    if (jobs) {
        return (
            <div className="jobs-page">
                <NavBar props={new Props(anchorList, true)} />

                <div className="card-section">
                    {jobs.map((job, index) => (
                        <div key={index} className="jobs-card">
                            <JobsCard
                                company={job['company']}
                                position={job['position']}
                                description={job['description']}
                                logo={job['logo']}
                                link={job['link']}
                            />
                        </div>
                    ))}
                </div>
                <Footer />
            </div>
        );
    }
};
