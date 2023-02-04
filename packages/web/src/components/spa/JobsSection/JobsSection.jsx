import { NavBar } from '../Navigation/NavBar';
import './jobs_section.css';
import { Anchor, Props } from '../Navigation/NavFactory';

const anchorList = [
    new Anchor('About', '/#about'),
    new Anchor('Events', '/#events'),
    new Anchor('Articles', '/#articles'),
    new Anchor('Team', '/#team'),
    new Anchor('Jobs', '/jobs')
];

export const JobsSection = () => {
    return (
        <div className="jobs-container">
            <NavBar props={new Props(anchorList, true, "transparent")} />
            <h1>WORKING</h1>
        </div>
    );
};
