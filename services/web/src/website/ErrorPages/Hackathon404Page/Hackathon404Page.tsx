export const Hackathon404Page = () => {
    return (
        <div className="relative min-h-screen w-full bg-white overflow-hidden flex items-center justify-center">
            <img
                src="/Hackathon404Page/left-bg.png"
                className="absolute left-0 top-0 h-full w-auto object-cover pointer-events-none"
            />

            <img
                src="/Hackathon404Page/right-bg.png"
                className="absolute right-0 bottom-0 h-full w-auto object-cover pointer-events-none"
            />

            <div className="relative z-10 flex items-center gap-[4.063rem]">
                <img src="/Hackathon404Page/hubzie.png" alt="Hubzie" className="w-[14.125rem] h-[20.25rem]" />

                <div className="flex flex-col">
                    <h1 className="text-[6rem] font-orbitron text-[#AA1616] leading-[1.25]">404</h1>

                    <h2 className="text-[1.5rem] font-oxanium text-[#000000] leading-[1.25]">
                        Something&apos;s missing
                    </h2>

                    <p className="text-[1rem] text-[#000000] font-oxanium leading-[1.25] mb-[1.063rem]">
                        This page is missing or you assembled the link incorrectly
                    </p>

                    <a
                        href="/hackathon"
                        className="text-[#AA1616] font-oxanium text-[0.875rem] leading-[1.25] underline hover:text-[#AA1616]"
                    >
                        Go to website &gt;
                    </a>
                </div>
            </div>
        </div>
    );
};
