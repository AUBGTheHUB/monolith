import logo from './images/hublogo.png';

const NAV_ITEM = 'py-[22.5px] px-[10px] text-lg';
const NAV_ITEM_A = 'text-white font-light';

export default function DesktopNav() {
    return (
        <div className="w-full">
            <div className="w-full flex flex-row align-top bg-[#07064d]">
                <div className="w-[45%] items-center">
                    <img src={logo} className="h-[70px] my-[15px] mx-auto" />
                </div>
                <div className="w-[55%] flex flex-row items-center">
                    <div className="mx-auto">
                        <span className={NAV_ITEM}>
                            <a href="#past-events" className={NAV_ITEM_A}>
                                Past Events
                            </a>
                        </span>
                        <span className={NAV_ITEM}>
                            <a href="#departments" className={NAV_ITEM_A}>
                                Departments
                            </a>
                        </span>
                        <span className={NAV_ITEM}>
                            <a href="#hackathon" className={NAV_ITEM_A}>
                                Hackathon
                            </a>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}
