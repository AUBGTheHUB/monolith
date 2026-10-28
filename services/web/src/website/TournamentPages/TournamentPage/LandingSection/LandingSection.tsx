export default function LandingSection() {
    return (
        <div className=" h-[80dvh] lg:h-[calc(80dvh-5rem)]">
            <div className="h-full flex flex-col justify-center items-center">
                <div className="w-fit max-w-[90%] flex flex-col gap-8 sm:gap-12">
                    <div className="font-semibold">
                        <h1 className="font-league font-bold text-[#F9DB98CF] text-2xl xs:text-3xl sm:text-4xl md:text-5xl xl:text-6xl">
                            THE HUB <span className="text-[#A9BCCE]">x</span>
                        </h1>
                        <h1 className="font-league font-bold text-[#C79B3B] text-2xl xs:text-3xl sm:text-4xl md:text-5xl xl:text-6xl">
                            LEAGUE OF LEGENDS
                        </h1>
                        <h3 className="flex font-semibold font-league items-center gap-3 w-full text-[#F9DB98CF] text-[10px] xs:text-xs sm:text-sm md:text-base xl:text-xl">
                            <span className="hidden md:block h-[2px] flex-1 bg-[#C79B3B]" />
                            <span className="md:whitespace-nowrap">ESPORTS CONFERENCE & GAMING TOURNAMENT</span>
                            <span className="hidden md:block h-[2px] flex-1 bg-[#C79B3B]" />
                        </h3>
                    </div>
                    <div className="w-0 min-w-[85%] text-[#90D5FF] text-xs sm:text-lg">
                        A one-day event that brings together the gaming community, industry professionals and passionate
                        players. Explore the latest in gaming through inspiring talks and discussions, and put your
                        skills to the test in an exciting League of Legends tournament.
                    </div>
                </div>
            </div>
        </div>
    );
}
