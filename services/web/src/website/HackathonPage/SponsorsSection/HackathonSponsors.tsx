type SponsorRank = 'Platinum' | 'Gold' | 'Silver';

function SponsorSection({ rank }: { rank: SponsorRank }) {
    const rankColor = rank === 'Platinum' ? '#19A0F0' : rank === 'Gold' ? '#FFDE06' : '#92B1C9';
    return (
        <div>
            <div className="text-xl py-4" style={{ color: rankColor }}>
                <h3>{rank}</h3>
            </div>
            <div className="w-full h-[1px] bg-[#233340] mb-10 relative">
                <div className="bg-[#AEC1D0] h-[1px] w-10 aboslute left-0"></div>
                <div className="bg-[#AEC1D0] h-[5px] w-[5px] absolute rounded-full right-0 top-[-2.5px]"></div>
                <div className="bg-[#AEC1D0] h-[5px] w-[5px] absolute rounded-full right-2 top-[-2.5px]"></div>
                <div className="bg-[#AEC1D0] h-[5px] w-[5px] absolute rounded-full right-4 top-[-2.5px]"></div>
            </div>
        </div>
    );
}

export default function HackathonSponsors() {
    return (
        <div className="text-white sm:w-[80%] mx-6 sm:mx-auto py-10 sm:py-20">
            <div className="text-3xl sm:text-4xl flex items-center gap-4 mb-20">
                <img src="./n.png" alt="" className="w-[1.6rem]" />
                <h2>Sponsors</h2>
            </div>
            <SponsorSection rank="Platinum" />
            <SponsorSection rank="Gold" />
            <SponsorSection rank="Silver" />
        </div>
    );
}
