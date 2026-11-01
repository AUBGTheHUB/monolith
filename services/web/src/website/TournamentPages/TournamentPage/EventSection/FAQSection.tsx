import community from './assets/community.png';
import euro from './assets/euro.png';
import location from './assets/location.png';
import calendar from './assets/calendar.png';

import FAQCard from './FAQCard';

export default function FAQSection() {
    return (
        <div id="faq" className="flex flex-col items-center gap-3 py-5 mx-6">
            <h4 className="text-[#C79B3B] text-xl md:text-2xl font-bold">EVENT INFORMATION</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 py-2 md:flex-row gap-7 justify-center wrap">
                <FAQCard question="When?" answer="November 15, 2026 (Sunday)" image={calendar} />
                <FAQCard question="Where?" answer="AUBG, ABF Building — Sports Hall" image={location} />
                <FAQCard question="How many players?" answer="8 teams, 5 players per team" image={community} />
                <FAQCard question="How much?" answer="5€ per person" image={euro} />
            </div>
        </div>
    );
}
