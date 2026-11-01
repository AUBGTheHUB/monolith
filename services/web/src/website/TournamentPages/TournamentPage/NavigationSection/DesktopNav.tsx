export const DesktopNavComponent = () => {
    const NAV_ITEM_A = 'text-[#C79B3B] font-semibold';
    const NAV_ITEM_A_EFFECT =
        'hover:text-white relative after:content-[""] after:absolute after:w-full after:scale-x-0 after:h-[2px] after:bottom-[-4px] after:left-0 after:bg-white after:origin-bottom-right after:transition-transform after:duration-300 hover:after:scale-x-100 hover:after:origin-bottom-left';

    return (
        <div className={`w-full h-[10%] bg-[#163B59] border-b-4 border-[#C79B3B] py-4 sticky top-0 z-[100]`}>
            <div className="w-full flex flex-row justify-center items-center">
                <div className="w-[8%] items-center z-10 flex justify-center"></div>
                <div className="flex flex-row w-[70%] gap-7">
                    <a href="/" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                        The HUB
                    </a>
                    <a href="#faq" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                        FAQ
                    </a>
                </div>
                <div>
                    <a
                        href="/tournament/registration"
                        className={`font-bold border-[#061F36] text-[#061F36] border-2 bg-[#C79B3B]  px-3 py-2 hover:text-[#061F36] hover:bg-[#C79B3B] transition-colors duration-500`}
                    >
                        REGISTER NOW
                    </a>
                </div>
            </div>
        </div>
    );
};
