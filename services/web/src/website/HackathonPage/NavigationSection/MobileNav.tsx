import hamburgerMenuIcon from '../../MainPage/Navigation/images/hamburger_menu.svg';
import logo from '../../MainPage/Navigation/images/hublogo.webp';
import about from './images/about.svg';
import schedule from './images/schedule.svg';
import grading from './images/grading.svg';
import faq from './images/faq.svg';
import participate from './images/participate.svg';
import { Sheet, SheetContent, SheetDescription, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { useEffect, useState } from 'react';

export const MobileNavComponent = () => {
    const NAV_ITEM_A = 'text-black hover:text-black';
    const NAV_ITEM = 'text-[18pt] text-left leading-[1.5em] my-4';
    const NAV_ITEM_IMG = 'mt-[5px] float-left mr-[9px] h-[25px] w-[25px] align-middle';
    const [isOpen, setIsOpen] = useState(false);
    const [fadeIn, setFadeIn] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => {
            setFadeIn(true);
        }, 400);

        return () => clearTimeout(timer);
    }, []);

    return (
        <nav
            className={`sticky h-[10vh] top-0 z-[50] bg-[rgba(0,0,0,0.5)] transform transition-all duration-1000 ease-in-out ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
            aria-label="Mobile Navigation"
        >
            <div className="flex justify-around items-center h-full">
                <a href="/">
                    <img src={logo} className="h-[50px]" />
                </a>
                <h2 className="text-white font-medium text-2xl mr-[10px]">The Hub</h2>
                <div className="h-[50px]">
                    <Sheet open={isOpen} onOpenChange={setIsOpen}>
                        <SheetTitle />
                        <SheetDescription />
                        <SheetTrigger className="h-[50px]">
                            <img src={hamburgerMenuIcon} onClick={() => setIsOpen(true)} />
                        </SheetTrigger>
                        <SheetContent onCloseAutoFocus={(event) => event.preventDefault()}>
                            <div className={NAV_ITEM}>
                                <a href="#about" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    <img src={about} className={NAV_ITEM_IMG} />
                                    About
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#schedule" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    <img src={schedule} className={NAV_ITEM_IMG} />
                                    Schedule
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#grading-criteria" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    <img src={grading} className={NAV_ITEM_IMG} />
                                    Grading Criteria
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#faq" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    <img src={faq} className={NAV_ITEM_IMG} />
                                    FAQ
                                </a>
                            </div>
                            <div className={`${NAV_ITEM}`}>
                                <img src={participate} className={`${NAV_ITEM_IMG}`} />
                                <a className="text-sky-600 hover:text-sky-600" href="/hackathon/registration">
                                    Participate now
                                </a>
                            </div>
                        </SheetContent>
                    </Sheet>
                </div>
            </div>
        </nav>
    );
};
