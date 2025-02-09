import hamburgerMenuIcon from '../../MainPage/Navigation/images/hamburger_menu.svg';
import logo from '../../MainPage/Navigation/images/hublogo.png';

import about from './images/about.svg';
import schedule from './images/schedule.svg';
import grading from './images/grading.svg';
import faq from './images/faq.svg';
import participate from './images/participate.svg';

import { Sheet, SheetContent, SheetDescription, SheetTitle, SheetTrigger } from '@/components/ui/sheet';

export const MobileNavComponent = () => {
    const NAV_ITEM_A = 'text-black hover:text-black';
    const NAV_ITEM = 'text-[18pt] text-left leading-[1.5em] my-4';
    const NAV_ITEM_IMG = 'mt-[5px] float-left mr-[9px] h-[25px] w-[25px] align-middle';

    return (
        <div className="navigation h-[10%]">
            <div className="nav-bar flex align-top bg-transparent">
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
                        <a href="#about" className={NAV_ITEM_A}>
                            <img src={about} className={NAV_ITEM_IMG} />
                            About
                        </a>
                    </div>
                    <div className={NAV_ITEM}>
                        <a href="#schedule" className={NAV_ITEM_A}>
                            <img src={schedule} className={NAV_ITEM_IMG} />
                            Schedule
                        </a>
                    </div>
                    <div className={NAV_ITEM}>
                        <a href="#grading-criteria" className={NAV_ITEM_A}>
                            <img src={grading} className={NAV_ITEM_IMG} />
                            Grading Criteria
                        </a>
                    </div>
                    <div className={NAV_ITEM}>
                        <a href="#faq" className={NAV_ITEM_A}>
                            <img src={faq} className={NAV_ITEM_IMG} />
                            FAQ
                        </a>
                    </div>
                    <div className={`${NAV_ITEM} flex`}>
                        <img src={participate} className={`${NAV_ITEM_IMG}`} />
                        <a
                            className="text-sky-600 rounded-2xl px-5 border border-sky-600 hover:bg-sky-600 hover:text-white transition-colors duration-500"
                            href="#participate-now"
                        >
                            Participate now
                        </a>
                    </div>
                </SheetContent>
            </Sheet>
        </div>
    );
};
