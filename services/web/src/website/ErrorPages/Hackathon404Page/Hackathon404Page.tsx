export const Hackathon404Page = () => {
    return (
        <div className="relative min-h-screen w-full bg-white overflow-hidden flex items-center justify-center px-4">
            <img
                src="/Hackathon404Page/left-bg.png"
                className="absolute left-0 top-0 h-full w-auto object-cover pointer-events-none"
            />

            <img
                src="/Hackathon404Page/right-bg.png"
                className="absolute right-0 bottom-0 h-full w-auto object-cover pointer-events-none"
            />

            <div className="relative z-10 flex flex-col md:flex-row items-center md:items-end gap-[2rem] md:gap-[4.063rem] lg:gap-[5rem]">
                <img
                    src="/Hackathon404Page/hubzie.png"
                    alt="Hubzie"
                    className="w-[10rem] h-[14rem] md:w-[14.125rem] md:h-[20.25rem] lg:w-[18rem] lg:h-[25.75rem]"
                />

                <div className="flex flex-col text-center md:text-left">
                    <h1 className="text-[4rem] md:text-[6rem] lg:text-[8rem] font-orbitron text-[#AA1616] leading-[1.25]">
                        404
                    </h1>

                    <h2 className="text-[1.25rem] md:text-[1.5rem] lg:text-[2rem] font-oxanium text-[#000000] leading-[1.25] mb-[1rem] lg:mb-[1.5rem]">
                        Something&apos;s missing
                    </h2>

                    <p className="text-[0.875rem] md:text-[1rem] lg:text-[1.25rem] text-[#000000] font-oxanium leading-[1.25] mb-[1rem] lg:mb-[1.5rem] max-w-[19.5rem] lg:max-w-[24rem]">
                        This page is missing or you assembled the link incorrectly
                    </p>

                    <a
                        href="/hackathon"
                        className="text-[#AA1616] hover:text-[#DC2626] font-oxanium text-[0.75rem] md:text-[0.875rem] lg:text-[1.125rem] leading-[1.25] underline"
                    >
                        Go to website &gt;
                    </a>
                </div>
            </div>
        </div>
    );
};
