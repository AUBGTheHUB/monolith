export const AwardsFooter = () => (
    <div className="flex flex-col items-center w-full relative z-30">
        <div className="flex flex-col lg:flex-row flex-wrap justify-between items-start w-full text-white text-base lg:text-[1.2vw] xl:text-2xl font-oxanium gap-6 lg:gap-8 xl:gap-16 mb-8 lg:mb-10 px-8 lg:px-[4vw] xl:px-32 leading-relaxed">
            <div className="flex-1 mb-4 lg:mb-0">
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
                    className="w-10 h-10 lg:w-[2.5vw] lg:h-[2.5vw] xl:w-14 xl:h-14 object-contain"
                />
            </div>
            <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true" />
        </div>
    </div>
);
