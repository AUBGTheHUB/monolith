import { CornerUpLeft } from 'lucide-react';
import hamburgerMenuIcon from '../../MainPage/Navigation/images/hamburger_menu.svg';
import logo from '../../MainPage/Navigation/images/hublogo.png';
import { Sheet, SheetContent, SheetDescription, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { useEffect, useState } from 'react';

export const MobileNavComponent = () => {
    const NAV_ITEM_A = 'text-black hover:text-black flex items-center';
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
            className={`sticky h-[10vh] top-0 z-[100] bg-[rgba(0,0,0,0.5)]" aria-label="Mobile Navigation  transform transition-all duration-1000 ease-in-out ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
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
                                <a href="/hackathon" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                    <CornerUpLeft className="pb-[2px] mr-[5px]" />
                                    Go back
                                </a>
                            </div>
                        </SheetContent>
                    </Sheet>
                </div>
            </div>
        </nav>
    );
};
