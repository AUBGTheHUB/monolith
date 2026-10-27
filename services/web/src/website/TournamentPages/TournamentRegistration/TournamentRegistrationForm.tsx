export default function TournamentRegistrationForm() {
    return (
        <div className="relative min-h-screen w-full bg-white overflow-hidden flex items-center justify-center px-4">
            <img
                src="/Tournament/hextech.png"
                alt="left background hextech image"
                className="absolute rotate-180 left-0 top-0 h-[40%] lg:h-[60%] w-auto object-cover pointer-events-none"
            />

            <img
                src="/Tournament/hextech.png"
                alt="Right background hextech image"
                className="absolute right-0 bottom-[0] h-[40%] lg:h-[60%] w-auto object-cover pointer-events-none"
            />

            <div className="relative z-10 flex flex-col md:flex-row items-center md:items-end gap-[2rem] md:gap-[4.063rem] lg:gap-[5rem]">
                <div className="flex flex-col text-center md:text-left">
                    <h1 className="text-[4rem] md:text-[6rem]  font-orbitron text-[#C79B3B] leading-[1.25]">
                        Expecting soon....
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
