export default function LandingSection() {
    return (
        <div className="bg-[#061F36] font-mont h-[80dvh] lg:h-[calc(80dvh-5rem)]">
            <div className="h-full gap-6 flex flex-col justify-center items-center">
                <div className="font-semibold w-[60%]">
                    <h1 className="text-[#F9DB98CF] text-4xl sm:text-6xl">
                        THE HUB <span className="text-[#A9BCCE]">x</span>
                    </h1>
                    <h1 className="text-[#C79B3B] text-4xl sm:text-6xl">LEAGUE OF LEGENDS</h1>
                    <h3 className="text-[#F9DB98CF] font-normal text-md sm:text-xl">
                        ESPORTS CONFERENCE & GAMING TOURNAMENT
                    </h3>
                </div>
                <div className="w-[60%] text-[#90D5FF] text-xs sm:text-lg">
                    A one-day event that brings together the gaming community, industry professionals and passionate
                    players. Explore the latest in gaming through inspiring talks and discussions, and put your skills
                    to the test in an exciting League of Legends tournament.
                </div>
            </div>
        </div>
    );
}
