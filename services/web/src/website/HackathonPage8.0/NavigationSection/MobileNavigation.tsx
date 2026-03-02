import hamburgerMenuIcon from '../../MainPage/Navigation/images/hamburger_menu.svg';
import logo from '../../MainPage/Navigation/images/hublogo.webp';
import { Sheet, SheetContent, SheetDescription, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { useEffect, useState } from 'react';

export const MobileNavigationComponent = () => {
    const NAV_ITEM_A = 'text-black hover:text-black font-orbitron';
    const NAV_ITEM = 'text-[18pt] text-left leading-[1.5em] my-4';
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
            className={`sticky h-[10vh] top-0 z-[50] bg-[rgba(28,26,25,0.9)] transform transition-all duration-1000 ease-in-out ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
            aria-label="Mobile Navigation"
        >
            <div className="flex px-2 justify-around items-center h-full">
                <a href="/">
                    <img src={logo} className="h-[50px]" />
                </a>
                <h2 className="text-[rgba(255,253,245,1)] font-medium text-2xl mr-[10px]">The Hub</h2>
                <div className="h-[50px]">
                    <Sheet open={isOpen} onOpenChange={setIsOpen}>
                        <SheetTitle />
                        <SheetDescription />
                        <SheetTrigger className="h-[50px]">
                            <img src={hamburgerMenuIcon} onClick={() => setIsOpen(true)} />
                        </SheetTrigger>
                        <SheetContent
                            className="bg-[rgba(255,253,245,1)]"
                            onCloseAutoFocus={(event) => event.preventDefault()}
                        >
                            <div className={NAV_ITEM}>
                                <a href="#mission" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    ABOUT
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#schedule" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    SCHEDULE
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#journey" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    JOURNEY
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#grading-criteria" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    GRADING CRITERIA
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#faq" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    FAQ
                                </a>
                            </div>
                            <div className={`${NAV_ITEM}`}>
                                <a
                                    className="text-[rgb(170,22,22)] font-orbitron hover:text-[rgb(170,22,22)]"
                                    href="/hackathon/registration"
                                >
                                    PARTICIPATE NOW
                                </a>
                            </div>
                        </SheetContent>
                    </Sheet>
                </div>
            </div>
        </nav>
    );
};
