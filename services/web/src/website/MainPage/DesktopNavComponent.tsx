import logo from './hublogo.png';

export function DesktopNavComponent() {
    return (
        <div className="nav-bar flex flex-row align-top">
            <div className="nav-section-left items-center">
                <img src={logo} className="logo" />
            </div>
            <div className="nav-section-right flex flex-row items-center">
                <div className="nav-items">
                    <span className="nav-text-item">
                        <a href="#past-events">Past Events</a>
                    </span>
                    <span className="nav-text-item">
                        <a href="#departments">Departments</a>
                    </span>
                    <span className="nav-text-item">
                        <a href="#hackathon">Hackathon</a>
                    </span>
                </div>
            </div>
        </div>
    );
}
