export const AwardsFooter = () => (
    <div className="flex flex-col items-center w-full relative z-30">
        <div className="flex flex-col lg:flex-row flex-wrap justify-between items-start w-full text-white text-[1.8vh] lg:text-[1.5vh] font-oxanium gap-[2vh] mb-[2vh] px-8 lg:px-[4vw] xl:px-32 leading-relaxed">
            <div className="flex-1 lg:max-w-[40%]">
                <p>And much more!</p>
                <p>Take part in all of the games we have prepared!</p>
            </div>
            <div className="flex-1 lg:text-right lg:max-w-[40%]">
                <p>All participants will receive giftbags with swag from The Hub and all HackAUBG 8.0 partners!</p>
            </div>
        </div>

        <div className="w-full flex items-center justify-center px-4 lg:px-8 xl:px-16">
            <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true" />
            <div className="mx-6 lg:mx-[2vw] xl:mx-16">
                <img
                    src="/AwardsSection/HackAUBG_8.0-Awards-Logo.png"
                    alt="HackAUBG logo"
                    className="w-[4vh] h-[4vh] lg:w-[4vh] lg:h-[4vh] object-contain"
                />
            </div>
            <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true" />
        </div>
    </div>
);
