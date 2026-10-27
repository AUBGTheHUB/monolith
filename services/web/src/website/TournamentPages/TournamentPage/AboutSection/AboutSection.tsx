import microphone from './assets/microphone.png';
import trophy from './assets/trophy.png';
import AboutCard from './components/AboutCard';

export default function AboutSection() {
    return (
        <div id="about" className="flex flex-col items-center gap-20 justify-around bg-[#061F36] font-mont px-10">
            <div className="flex flex-col md:flex-row md:items-stretch items-center justify-center gap-20">
                <AboutCard
                    title="THE CONFERENCE"
                    description="Inspiring talks, panel discussions and insights from industry professionals, game developers and creators."
                    image={`${microphone}`}
                />
                <AboutCard
                    title="THE TOURNAMENT"
                    description="Team up, compete in League of Legends and show off your skills in an exciting tournament."
                    image={`${trophy}`}
                />
            </div>
            <div className="flex justify-center gap-2 sm:gap-4">
                <img src="/Tournament/chain.png" className="h-6 xs:h-8 w-auto sm:h-12" alt="Chain" />
                <img src="/Tournament/chain.png" className="h-6 xs:h-8 w-auto sm:h-12 rotate-180" alt="Chain" />
            </div>
        </div>
    );
}
