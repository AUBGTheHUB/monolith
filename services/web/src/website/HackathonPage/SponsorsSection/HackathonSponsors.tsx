import { Sponsors } from './constants';

type SponsorRank = 'Platinum' | 'Gold' | 'Silver';

export interface HackathonSponsorProps {
    rank: SponsorRank;
    name: string;
    logoSrc: string;
}

function SponsorCard({ sponsor }: { sponsor: HackathonSponsorProps }) {
    return (
        <div className="border border-[#233340] bg-white rounded-lg min-w-40 max-w-60 min-h-10 aspect-square w-full sm:w-1/5 p-4">
            <img src={sponsor.logoSrc} alt={sponsor.name} className="w-full h-full object-contain" />
        </div>
    );
}

function SponsorSection({ rank, sponsors }: { rank: SponsorRank; sponsors: HackathonSponsorProps[] }) {
    const rankColor = rank === 'Platinum' ? '#19A0F0' : rank === 'Gold' ? '#FFDE06' : '#92B1C9';
    return (
        <div className="pb-20">
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
            <div className="flex flex-wrap gap-2 justify-center sm:justify-start">
                {sponsors.map((sponsor) => (
                    <SponsorCard sponsor={sponsor} key={sponsor.name} />
                ))}
            </div>
        </div>
    );
}

export default function HackathonSponsors() {
    // Filter the sponsors
    const platinumSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Platinum');
    const goldSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Gold');
    const silverSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Silver');

    //Sort each category alphabetically
    platinumSponsors.sort((a, b) => a.name.localeCompare(b.name));
    goldSponsors.sort((a, b) => a.name.localeCompare(b.name));
    silverSponsors.sort((a, b) => a.name.localeCompare(b.name));

    return (
        <div className="text-white sm:w-[80%] mx-6 sm:mx-auto py-10 sm:py-20">
            <div className="text-3xl sm:text-4xl flex items-center gap-4 mb-20">
                <img src="./n.png" alt="" className="w-[1.6rem]" />
                <h2>Sponsors</h2>
            </div>
            <SponsorSection rank="Platinum" sponsors={platinumSponsors} />
            <SponsorSection rank="Gold" sponsors={goldSponsors} />
            <SponsorSection rank="Silver" sponsors={silverSponsors} />
        </div>
    );
}
