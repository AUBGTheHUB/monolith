import logo from './images/hublogo.png';

const NAV_ITEM = 'py-[22.5px] px-[20px] text-lg ';
const NAV_ITEM_A =
    'text-white font-light hover:text-white relative after:content-[""] after:absolute after:w-full after:scale-x-0 after:h-[2px] after:bottom-[-4px] after:left-0 after:bg-white after:origin-bottom-right after:transition-transform after:duration-300 hover:after:scale-x-100 hover:after:origin-bottom-left';

export default function DesktopNav() {
    return (
        <div className="w-full">
            <div className="w-full flex flex-row align-top bg-transparent">
                <div className="w-[42%] items-center">
                    <a href="/">
                        <img src={logo} className="h-[70px] my-[15px] mx-auto" />
                    </a>
                </div>
                <div className="w-[58%] flex flex-row items-center">
                    <div className="mx-auto flex">
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
