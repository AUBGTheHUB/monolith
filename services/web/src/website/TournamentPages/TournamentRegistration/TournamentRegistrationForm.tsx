export default function TournamentRegistrationForm() {
    return (
        <div className="relative min-h-screen w-full bg-white overflow-hidden flex items-center justify-center px-4">
            <div className="hidden xs:block absolute right-0 top-[68%] h-[34dvh] sm:h-[40dvh] lg:h-[70dvh] translate-x-1/2 -translate-y-1/2 opacity-40 sm:opacity-60 lg:opacity-100 pointer-events-none z-0">
                <img
                    src="/Tournament/hextech.png"
                    alt=""
                    className="h-full w-auto max-w-none object-contain animate-spin [animation-duration:60s]"
                />
            </div>
            <div className="absolute left-0 top-[30%] h-[50dvh] lg:h-[70dvh] -translate-x-1/2 -translate-y-1/2 -scale-x-100 pointer-events-none z-0">
                <img
                    src="/Tournament/hextech.png"
                    alt=""
                    className="h-full w-auto max-w-none object-contain animate-spin [animation-duration:60s] [animation-direction:reverse]"
                />
            </div>
            <div className="relative z-10 flex flex-col md:flex-row items-center md:items-end gap-[2rem] md:gap-[4.063rem] lg:gap-[5rem]">
                <div className="flex flex-col text-center md:text-left">
                    <h1 className="text-[4rem] md:text-[6rem]  font-orbitron text-[#C79B3B] leading-[1.25]">
                        Coming soon....
                    </h1>

                    <a
                        href="/tournament"
                        className="text-[#C79B3B] hover:text-[#DC2626] font-oxanium text-[0.75rem] md:text-[0.875rem] lg:text-[1.125rem] leading-[1.25] underline"
                    >
                        Go to tournament &gt;
                    </a>
                </div>
            </div>
        </div>
    );
}
