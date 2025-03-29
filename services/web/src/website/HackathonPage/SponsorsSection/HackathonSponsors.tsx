import { Sponsors } from './constants';

type SponsorRank = 'Platinum' | 'Gold' | 'Silver' | 'Bronze' | 'Custom';

export interface HackathonSponsorProps {
    rank: SponsorRank;
    name: string;
    logoSrc: string;
    websiteLink: string;
}

function SponsorCard({ sponsor, rank }: { sponsor: HackathonSponsorProps; rank: SponsorRank }) {
    return (
        <a
            className={`block border border-[#233340] bg-white rounded-lg min-w-40 max-w-60 min-h-10 aspect-square w-full sm:w-1/5 p-4 cursor-pointer transition-shadow duration-400 hover:shadow-md ${rank === 'Platinum' ? 'hover:shadow-[#19A0F0]' : rank === 'Gold' ? 'hover:shadow-[#FFDE06]' : rank === 'Silver' ? 'hover:shadow-[#92B1C9]' : 'hover:shadow-[#CD7F32]'}`}
            href={sponsor.websiteLink}
            target="_blank"
            rel="noreferrer"
        >
            <img src={sponsor.logoSrc} alt={sponsor.name} className="w-full h-full object-contain" />
        </a>
    );
}

function SponsorSection({ rank, sponsors }: { rank: SponsorRank; sponsors: HackathonSponsorProps[] }) {
    const rankColor =
        rank === 'Platinum'
            ? '#19A0F0'
            : rank === 'Gold'
              ? '#FFDE06'
              : rank === 'Silver'
                ? '#92B1C9'
                : rank === 'Bronze'
                  ? '#CD7F32'
                  : '#FFFFFF';
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
                    <SponsorCard sponsor={sponsor} key={sponsor.name} rank={rank} />
                ))}
            </div>
        </div>
    );
}

export default function HackathonSponsors({ sponsorsSwitch }: { sponsorsSwitch: boolean }) {
    // Filter the sponsors
    const platinumSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Platinum');
    const goldSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Gold');
    const silverSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Silver');
    const bronzeSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Bronze');
    const customSponsors = Sponsors.filter((sponsor) => sponsor.rank === 'Custom');

    //Sort each category alphabetically
    platinumSponsors.sort((a, b) => a.name.localeCompare(b.name));
    goldSponsors.sort((a, b) => a.name.localeCompare(b.name));
    silverSponsors.sort((a, b) => a.name.localeCompare(b.name));
    bronzeSponsors.sort((a, b) => a.name.localeCompare(b.name));
    customSponsors.sort((a, b) => a.name.localeCompare(b.name));

    if (sponsorsSwitch) {
        return (
            <div className="text-white sm:w-[80%] mx-6 sm:mx-auto py-10 sm:py-20">
                <div className="text-3xl sm:text-4xl flex items-center gap-4 mb-20">
                    <img src="./n.webp" alt="" className="w-[1.6rem]" />
                    <h2>Sponsors</h2>
                </div>
                <SponsorSection rank="Platinum" sponsors={platinumSponsors} />
                <SponsorSection rank="Gold" sponsors={goldSponsors} />
                <SponsorSection rank="Silver" sponsors={silverSponsors} />
                <SponsorSection rank="Bronze" sponsors={bronzeSponsors} />
                {/* <SponsorSection rank="Custom" sponsors={customSponsors} /> */}
            </div>
        );
    } else {
        return (
            <div className="text-white sm:w-[80%] mx-6 sm:mx-auto py-10 sm:py-20">
                <div className="text-3xl sm:text-4xl flex items-center gap-4">
                    <img src="./n.webp" alt="" className="w-[1.6rem]" />
                    <h2 className="tracking-[0.2em]">SPONSORS COMING SOON . . .</h2>
                </div>
            </div>
        );
    }
}
