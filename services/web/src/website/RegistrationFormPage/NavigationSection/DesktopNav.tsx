import { CornerUpLeft } from 'lucide-react';
import logo from './images/hublogo.png';

export const DesktopNavComponent = () => {
    const NAV_ITEM_A = 'text-white font-light font-mont';
    const NAV_ITEM_A_EFFECT =
        'hover:text-white relative after:content-[""] after:absolute after:w-full after:scale-x-0 after:h-[2px] after:bottom-[-4px] after:left-0 after:bg-white after:origin-bottom-right after:transition-transform after:duration-300 hover:after:scale-x-100 hover:after:origin-bottom-left';
    return (
        <div className="w-full h-[10%] bg-[rgba(0,0,0,0.5)] border-gray-600 py-2 sticky top-0 z-[100]">
            <div className="w-full flex flex-row justify-center items-center">
                <div className="w-[8%] items-center z-10 flex justify-center">
                    <a href="/" className="cursor-pointer ">
                        <img src={logo} className="h-[50px] my-[15px]" />
                    </a>
                </div>
                <div className="flex flex-row w-[70%] gap-7"></div>
                <div>
                    <a href="/hackathon" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                        <CornerUpLeft />
                        Go back
                    </a>
                </div>
            </div>
        </div>
    );
};
