import hamburgerMenuIcon from '../../../MainPage/Navigation/images/hamburger_menu.svg';
import { Sheet, SheetContent, SheetDescription, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { useEffect, useState } from 'react';

export const MobileNavComponent = () => {
    const NAV_ITEM_A = 'text-[#C79B3B] hover:text-black';
    const NAV_ITEM = 'text-[18pt] text-left leading-[1.5em] my-4';
    const [isOpen, setIsOpen] = useState(false);
    const [fadeIn, setFadeIn] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => {
            setFadeIn(true);
        }, 400);

        return () => clearTimeout(timer);
    }, []);

    const maskStyle = (src: string): React.CSSProperties => ({
        backgroundColor: '#C79B3B',
        WebkitMask: `url(${src}) center / contain no-repeat`,
        mask: `url(${src}) center / contain no-repeat`,
    });

    return (
        <nav
            className={`sticky h-[10vh] top-0 z-[50] bg-[#163B59] transform transition-all duration-1000 ease-in-out ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
            aria-label="Mobile Navigation"
        >
            <div className="flex justify-around items-center h-full">
                <h2 className="text-[#C79B3B] text-center font-medium text-2xl mr-[10px]">The Hub</h2>
                <div className="h-[50px]">
                    <Sheet open={isOpen} onOpenChange={setIsOpen}>
                        <SheetTitle />
                        <SheetDescription />
                        <SheetTrigger className="h-[50px] w-[50px]">
                            <div className="h-full w-full" style={maskStyle(hamburgerMenuIcon)} />
                        </SheetTrigger>
                        <SheetContent onCloseAutoFocus={(event) => event.preventDefault()}>
                            <div className={NAV_ITEM}>
                                <a href="#about" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    About
                                </a>
                            </div>
                            <div className={NAV_ITEM}>
                                <a href="#faq" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    FAQ
                                </a>
                            </div>
                            <div className={`${NAV_ITEM}`}>
                                <a className="text-[#061F36] hover:text-sky-600" href="/hackathon/registration">
                                    REGISTER NOW
                                </a>
                            </div>
                        </SheetContent>
                    </Sheet>
                </div>
            </div>
        </nav>
    );
};
