import logo from './images/hublogo.png';
import hamburgerMenuIcon from './images/hamburger_menu.svg';
import photoIcon from './images/past_events.svg';
import threeDots from './images/departments.svg';
import codeIcon from './images/hackathon.svg';
import { Sheet, SheetContent, SheetDescription, SheetTitle, SheetTrigger, SheetClose } from '@/components/ui/sheet';
import { useState } from 'react';

const NAV_ITEM_A = 'text-black hover:text-black';
const NAV_ITEM = 'text-[18pt] text-left leading-[1.5em] my-4';
const NAV_ITEM_IMG = 'mt-[5px] float-left mr-[9px] h-[25px] w-[25px] align-middle';

export default function MobileNavComponent() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="navigation h-[10%]">
            <div className="nav-bar flex align-top bg-transparent">
                <div className="items-left">
                    <a href="/">
                        <img src={logo} className="h-[70px] m-[15px]" />
                    </a>
                </div>
            </div>
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
                <SheetTitle />
                <SheetDescription />
                <SheetTrigger>
                    <img
                        className="absolute right-[15px] top-[25px] h-[50px] text-right"
                        src={hamburgerMenuIcon}
                        onClick={() => setIsOpen(true)}
                    />
                </SheetTrigger>
                <SheetContent onCloseAutoFocus={(event) => event.preventDefault()}>
                    <div className={NAV_ITEM}>
                        <SheetClose asChild>
                            <a href="#past-events" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                                <img src={photoIcon} className={NAV_ITEM_IMG} />
                                Past Events
                            </a>
                        </SheetClose>
                    </div>
                    <div className={NAV_ITEM}>
                        <a href="#meet-team" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                            <img src={threeDots} className={NAV_ITEM_IMG} />
                            Departments
                        </a>
                    </div>
                    <div className={NAV_ITEM}>
                        <a href="/hackathon" className={NAV_ITEM_A} onClick={() => setIsOpen(false)}>
                            <img src={codeIcon} className={NAV_ITEM_IMG} />
                            Hackathon
                        </a>
                    </div>
                </SheetContent>
            </Sheet>
        </div>
    );
}
