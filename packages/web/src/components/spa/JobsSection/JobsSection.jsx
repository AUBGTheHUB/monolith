import { NavBar } from '../Navigation/NavBar';
import './jobs_section.css';
import { Anchor, Props } from '../Navigation/NavFactory';
import img1 from '../JobsSection/images/Vergil_4.jpeg';
import img2 from '../JobsSection/images/Vergil_5.jpg';
import img3 from '../JobsSection/images/Vergil_6.jpg';

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
            <NavBar props={new Props(anchorList, true)} />
            <div className='searchBar'>
                <div className='box'>
                <input type="text" placeholder='Search...'/>
                </div>
            </div>
            <div className='jobs'>
                <div className='job-box'>
                    <div className='photo'>
                        <img src={img1} alt="" />
                    </div>
                    <div className='text'>
                        <span>UI/ UX Designer</span>
                    </div>
                    <div className='text-2'>
                        <span> The User Experience Designer position exists 
                            to create compelling and elegant
                                digital user 
                                experiences through design...
                             </span>
                    </div>
                    <div className='button-container'>
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>                       
                    </div>
                    <div className='button-container'>
                        <button>Apply Now</button>
                        <button>Message</button>                       
                    </div>
                </div>
                <div className='job-box'>
                    <div className='photo'>
                        <img src={img2} alt="" />
                    </div>
                    <div className='text'>
                        <span>Sr. Product Designer</span>
                    </div>
                    <div className='text-2'>
                        <span> The User Experience Designer position exists 
                            to create compelling and elegant
                                digital user experiences through design...
                             </span>
                    </div>
                    <div className='button-container'>
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>                       
                    </div>
                    <div className='button-container'>
                        <button>Apply Now</button>
                        <button>Message</button>    
                    </div>
                </div>
                <div className='job-box'>
                    <div className='photo'>
                        <img src={img3} alt="" />
                    </div>
                    <div className='text'>
                        <span>User Experience Designer</span>
                    </div>
                    <div className='text-2'>
                        <span> The User Experience Designer position exists 
                            to create compelling and elegant
                                digital user experiences through design...
                             </span>
                    </div>
                    <div className='button-container'>
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>                       
                    </div>
                    <div className='button-container'>
                        <button>Apply Now</button>
                        <button>Message</button>    
                    </div>
                </div>
            </div>
            <div className='jobs'>
                <div className='job-box'>
                    <div className='photo'>
                        <img src={img1} alt="" />
                    </div>
                    <div className='text'>
                        <span>Product Designer</span>
                    </div>
                    <div className='text-2'>
                        <span> The User Experience Designer position exists 
                            to create compelling and elegant
                                digital user experiences through design...
                             </span>
                    </div>
                    <div className='button-container'>
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>                       
                    </div>
                    <div className='button-container'>
                        <button>Apply Now</button>
                        <button>Message</button>    
                    </div>
                </div>
                <div className='job-box'>
                    <div className='photo'>
                        <img src={img2} alt="" />
                    </div>
                    <div className='text'>
                        <span>UX Designer</span>
                    </div>
                    <div className='text-2'>
                        <span> The User Experience Designer position exists 
                            to create compelling and elegant
                                digital user experiences through design...
                             </span>
                    </div>
                    <div className='button-container'>
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>                       
                    </div>
                    <div className='button-container'>
                        <button>Apply Now</button>
                        <button>Message</button>    
                    </div>
                </div>
                <div className='job-box'>
                    <div className='photo'>
                        <img src={img3} alt="" />
                    </div>
                    <div className='text'>
                        <span>UI/ UX Designer</span>
                    </div>
                    <div className='text-2'>
                        <span> The User Experience Designer position exists 
                            to create compelling and elegant
                                digital user experiences through design...
                             </span>
                    </div>
                    <div className='button-container'>
                        <span>Full Time</span>
                        <span>Min. 1 Year</span>
                        <span>Senior Level</span>                       
                    </div>
                    <div className='button-container'>
                        <button>Apply Now</button>
                        <button>Message</button>    
                    </div>
                </div>
            </div>
        </div>
    );
};
