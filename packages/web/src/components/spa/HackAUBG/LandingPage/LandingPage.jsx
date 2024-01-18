import { LandingBackground } from '../LandingBackground/Background';
import './landing_page.css';
export const LandingPage = () => {
    return (
        <div className="landing-page">
            <LandingBackground />
            <div className="title">
                <h1>HACKAUBG 6.0</h1>
                <h2>31st March - 2nd April, AUBG - Blagoevgrad</h2>
                <button className="register-button">
                    <h1>Register</h1>
                    <svg width="20" height="25" viewBox="0 0 20 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M1.92298 25L1.92298 23.4042L4.23071 23.4042L4.23072 21.8087L6.53845 21.8087L6.53845 20.2128L8.84619 20.2128L8.84619 18.6173L11.1538 18.6173L11.1538 17.2873L13.4615 17.2873L13.4615 15.9575L15.7692 15.9575L15.7692 14.628L18.0769 14.628L18.0769 13.298L20 13.298L20 11.7022L18.0769 11.7022L18.0769 10.3722L15.7693 10.3722L15.7693 9.04297L13.4615 9.04297L13.4615 7.71297L11.1539 7.71297L11.1539 6.38321L8.84619 6.38321L8.84619 4.78741L6.53845 4.78741L6.53845 3.19185L4.23071 3.19185L4.23071 1.59605L1.92297 1.59604L1.92297 5.75475e-05L7.90761e-06 5.73794e-05L5.72205e-06 25L1.92298 25Z"
                            fill="white"
                        />
                        <mask
                            id="mask0_216_306"
                            style={{ maskType: 'alpha' }}
                            maskUnits="userSpaceOnUse"
                            x="0"
                            y="0"
                            width="20"
                            height="25">
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M1.92298 25L1.92298 23.4042L4.23071 23.4042L4.23072 21.8087L6.53845 21.8087L6.53845 20.2128L8.84619 20.2128L8.84619 18.6173L11.1538 18.6173L11.1538 17.2873L13.4615 17.2873L13.4615 15.9575L15.7692 15.9575L15.7692 14.628L18.0769 14.628L18.0769 13.298L20 13.298L20 11.7022L18.0769 11.7022L18.0769 10.3722L15.7693 10.3722L15.7693 9.04297L13.4615 9.04297L13.4615 7.71297L11.1539 7.71297L11.1539 6.38321L8.84619 6.38321L8.84619 4.78741L6.53845 4.78741L6.53845 3.19185L4.23071 3.19185L4.23071 1.59605L1.92297 1.59604L1.92297 5.75475e-05L7.90761e-06 5.73794e-05L5.72205e-06 25L1.92298 25Z"
                                fill="white"
                            />
                        </mask>
                        <g mask="url(#mask0_216_306)">
                            <rect
                                x="21.4286"
                                y="11.1702"
                                width="25"
                                height="11.36"
                                transform="rotate(-180 21.4286 11.1702)"
                                fill="#DBBFFF"
                            />
                        </g>
                    </svg>
                </button>
            </div>
        </div>
    );
};
