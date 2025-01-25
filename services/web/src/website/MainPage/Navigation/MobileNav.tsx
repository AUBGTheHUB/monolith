import logo from './images/hublogo.png';
import hamburgerMenuIcon from './images/hamburger_menu.svg';
import photoIcon from './images/past_events.svg';
import threeDots from './images/departments.svg';
import codeIcon from './images/hackathon.svg';
import './navigation.css';
import { Sheet, SheetContent, SheetHeader, SheetTrigger } from '@/components/ui/sheet';

const A = 'text-black';
const B = 'text-[18pt] text-left leading-[1.5em]';
const C = 'mt-[5px] float-left mr-[9px] h-[25px] w-[25px] align-middle';

export default function MobileNavComponent() {
    return (
        <div className="navigation">
            <div className="nav-bar flex align-top bg-cyan-200">
                <div className="items-left">
                    <img src={logo} className="h-[70px] m-[15px]" />
                </div>
            </div>
            <Sheet>
                <SheetTrigger>
                    <img className="absolute right-[15px] top-[25px] h-[50px] text-right" src={hamburgerMenuIcon} />
                </SheetTrigger>
                <SheetContent>
                    <SheetHeader></SheetHeader>
                    <br />
                    <div className={B}>
                        <a href="#past-events" className={A}>
                            <img src={photoIcon} className={C} />
                            Past Events
                        </a>
                    </div>
                    <br />
                    <div className={B}>
                        <a href="#departments" className={A}>
                            <img src={threeDots} className={C} />
                            Departments
                        </a>
                    </div>
                    <br />
                    <div className={B}>
                        <a href="#hackathon" className={A}>
                            <img src={codeIcon} className={C} />
                            Hackathon
                        </a>
                    </div>
                </SheetContent>
            </Sheet>
        </div>
    );
}
