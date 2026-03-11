export const Global404Page = () => {
    return (
        <div className="relative min-h-screen w-full bg-gradient-to-b to-[#071123] from-[#0A152C] overflow-hidden flex items-center justify-center px-4">
            <div className="relative z-10 flex flex-col md:flex-row items-center md:items-end gap-[2rem] md:gap-[4.063rem] lg:gap-[5rem]">
                <img
                    src="/Main404Page/Hubzie.png"
                    alt="Hubzie"
                    className="w-[10rem] h-[14rem] md:w-[14.125rem] md:h-[20.25rem] lg:w-[18rem] lg:h-[25.75rem]"
                />

                <div className="flex flex-col text-center md:text-left">
                    <h1 className="text-[4rem] md:text-[6rem] lg:text-[8rem] font-orbitron text-[#3A9ECD] leading-[1.25]">
                        404
                    </h1>

                    <h2 className="text-[1.25rem] md:text-[1.5rem] lg:text-[2rem] font-oxanium text-[#FFFFFF] leading-[1.25] mb-[1rem] lg:mb-[1.5rem]">
                        Something&apos;s missing
                    </h2>

                    <p className="text-[0.875rem] md:text-[1rem] lg:text-[1.25rem] text-[#FFFFFF] font-oxanium leading-[1.25] mb-[1rem] lg:mb-[1.5rem] max-w-[19.5rem] lg:max-w-[24rem]">
                        This page is missing or you assembled the link incorrectly
                    </p>

                    <a
                        href="/"
                        className="text-[#37A5D8] hover:text-[#009CF9] font-oxanium text-[0.75rem] md:text-[0.875rem] lg:text-[1.125rem] leading-[1.25] underline"
                    >
                        Go to website &gt;
                    </a>
                </div>
            </div>
        </div>
    );
};
