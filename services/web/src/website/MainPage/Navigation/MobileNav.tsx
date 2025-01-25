import logo from './images/hublogo.png';
import hamburgerMenuIcon from './images/hamburger_menu.svg';
import photoIcon from './images/past_events.svg';
import threeDots from './images/departments.svg';
import codeIcon from './images/hackathon.svg';
import { Sheet, SheetContent, SheetDescription, SheetTitle, SheetTrigger } from '@/components/ui/sheet';

const NAV_ITEM_A = 'text-black hover:text-black';
const NAV_ITEM = 'text-[18pt] text-left leading-[1.5em] my-4';
const NAV_ITEM_IMG = 'mt-[5px] float-left mr-[9px] h-[25px] w-[25px] align-middle';

export default function MobileNavComponent() {
    return (
        <div className="navigation">
            <div className="nav-bar flex align-top bg-[#07064d]">
                <div className="items-left">
                    <a href="/">
                        <img src={logo} className="h-[70px] m-[15px]" />
                    </a>
                </div>
            </div>
            <Sheet>
                <SheetTitle />
                <SheetDescription />
                <SheetTrigger>
                    <img className="absolute right-[15px] top-[25px] h-[50px] text-right" src={hamburgerMenuIcon} />
                </SheetTrigger>
                <SheetContent>
                    <div className={NAV_ITEM}>
                        <a href="#past-events" className={NAV_ITEM_A}>
                            <img src={photoIcon} className={NAV_ITEM_IMG} />
                            Past Events
                        </a>
                    </div>
                    <div className={NAV_ITEM}>
                        <a href="#departments" className={NAV_ITEM_A}>
                            <img src={threeDots} className={NAV_ITEM_IMG} />
                            Departments
                        </a>
                    </div>
                    <div className={NAV_ITEM}>
                        <a href="#hackathon" className={NAV_ITEM_A}>
                            <img src={codeIcon} className={NAV_ITEM_IMG} />
                            Hackathon
                        </a>
                    </div>
                </SheetContent>
            </Sheet>
        </div>
    );
}
