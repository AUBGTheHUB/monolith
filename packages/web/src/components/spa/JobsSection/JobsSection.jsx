import { NavBar } from '../Navigation/NavBar';
import './jobs_section.css';
import { Anchor, Props } from '../Navigation/NavFactory';
import img1 from '../JobsSection/images/amplify.png';
import img2 from '../JobsSection/images/droxic.png';
import img3 from '../JobsSection/images/paysafe.png';
import img4 from '../JobsSection/images/progress.png';
import img5 from '../JobsSection/images/vmware.png';
import img6 from '../JobsSection/images/uber_gold.png';

const anchorList = [
    new Anchor('About', '/#about'),
    new Anchor('Team', '/#team'),
    new Anchor('Jobs', '/jobs')
];

export const JobsSection = () => {
    return (
        <div className="jobs-container">
            <NavBar props={new Props(anchorList, true)} />
            <div className="jobs-box-container">
                <div className="job-box">
                    <div className="jobs-photo-container">
                        <a href="https://amplifyanalytix.com/" target="_blank">
                            <img src={img1} alt="" />
                        </a>
                    </div>
                    <div className="jobs-text-description-1">
                        <span>UI/ UX Designer</span>
                    </div>
                    <div className="jobs-text-description-2">
                        <span>
                            {' '}
                            The User Experience Designer position exists to
                            create compelling and elegant digital user
                            experiences through design...
                        </span>
                    </div>
                    <div className="jobs-button-container">
                        <span>Internship</span>
                        <span>Min. 1 Year</span>
                        <span>Junior Level</span>
                    </div>
                    <div className="jobs-button-container">
                        <button>Apply Now</button>
                    </div>
                </div>
                <div className="job-box">
                    <div className="jobs-photo-container">
                        <a href="https://droxic.com/en/" target="_blank">
                            <img src={img2} alt="" />
                        </a>
                    </div>
                    <div className="jobs-text-description-1">
                        <span>Sr. Product Designer</span>
                    </div>
                    <div className="jobs-text-description-2">
                        <span>
                            {' '}
                            The User Experience Designer position exists to
                            create compelling and elegant digital user
                            experiences through design...
                        </span>
                    </div>
                    <div className="jobs-button-container">
                        <span>Part-Time</span>
                        <span>Min. 2 Year</span>
                        <span>Mid Level</span>
                    </div>
                    <div className="jobs-button-container">
                        <button>Apply Now</button>
                    </div>
                </div>
                <div className="job-box">
                    <div className="jobs-photo-container">
                        <a
                            href="https://www.paysafe.com/eu-en/"
                            target="_blank"
                        >
                            <img src={img3} alt="" />
                        </a>
                    </div>
                    <div className="jobs-text-description-1">
                        <span>User Experience Designer</span>
                    </div>
                    <div className="jobs-text-description-2">
                        <span>
                            {' '}
                            The User Experience Designer position exists to
                            create compelling and elegant digital user
                            experiences through design...
                        </span>
                    </div>
                    <div className="jobs-button-container">
                        <span>Full Time</span>
                        <span>Min. 3 Year</span>
                        <span>Senior Level</span>
                    </div>
                    <div className="jobs-button-container">
                        <button>Apply Now</button>
                    </div>
                </div>
            </div>
            <div className="jobs-box-container">
                <div className="job-box">
                    <div className="jobs-photo-container">
                        <a href="https://www.progress.com/" target="_blank">
                            <img src={img4} alt="" />
                        </a>
                    </div>
                    <div className="jobs-text-description-1">
                        <span>Product Designer</span>
                    </div>
                    <div className="jobs-text-description-2">
                        <span>
                            {' '}
                            The User Experience Designer position exists to
                            create compelling and elegant digital user
                            experiences through design...
                        </span>
                    </div>
                    <div className="jobs-button-container">
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>
                    </div>
                    <div className="jobs-button-container">
                        <button>Apply Now</button>
                    </div>
                </div>
                <div className="job-box">
                    <div className="jobs-photo-container">
                        <a href="https://www.vmware.com//" target="_blank">
                            <img src={img5} alt="" />
                        </a>
                    </div>
                    <div className="jobs-text-description-1">
                        <span>UX Designer</span>
                    </div>
                    <div className="jobs-text-description-2">
                        <span>
                            {' '}
                            The User Experience Designer position exists to
                            create compelling and elegant digital user
                            experiences through design...
                        </span>
                    </div>
                    <div className="jobs-button-container">
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>
                    </div>
                    <div className="jobs-button-container">
                        <button>Apply Now</button>
                    </div>
                </div>
                <div className="job-box">
                    <div className="jobs-photo-container">
                        <a href="https://www.uber.com/ro/en/" target="_blank">
                            <img src={img6} alt="" />
                        </a>
                    </div>
                    <div className="jobs-text-description-1">
                        <span>UI/ UX Designer</span>
                    </div>
                    <div className="jobs-text-description-2">
                        <span>
                            {' '}
                            The User Experience Designer position exists to
                            create compelling and elegant digital user
                            experiences through design...
                        </span>
                    </div>
                    <div className="jobs-button-container">
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>
                    </div>
                    <div className="jobs-button-container">
                        <button>Apply Now</button>
                    </div>
                </div>
            </div>
        </div>
    );
};
