import JuryModule from '../../JurySection/components/JuryModule';
import mentors from '../StaticContent/mentors.json';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/base.css';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/embla-jury.css';
import EmblaCarousel from '@/components/EmblaCarousel/SlidesPerViewCarousel/js/EmblaCarousel.tsx';
import { EmblaOptionsType } from 'embla-carousel';

const OPTIONS: EmblaOptionsType = {
    breakpoints: {
        '(max-width: 600px)': {
            // Small screens (Mobile)
            align: 'center',
            slidesToScroll: 1,
        },
        '(min-width: 600px) and (max-width: 1500px)': {
            // Medium screens (Tablets)
            align: 'center',
            slidesToScroll: 3,
        },
        '(min-width: 1500px)': {
            // Large screens (Desktops)
            align: 'center',
            slidesToScroll: 4,
        },
    },
};

export default function MentorsSection() {
    const SLIDES = mentors.map((mentor, index) => (
        <JuryModule imgSrc={mentor.picture} name={mentor.name} company={mentor.company} job={mentor.job} key={index} />
    ));

    return (
        <div className="bg-[#000912] py-10">
            <div className=" space-y-7 font-mont sm:w-11/12 w-11/12 ml-auto z-10 relative ">
                <img src="/mentors/mentors_title.svg"></img>
                <img className="w-[90%]" src="/jury/jury_page_break.svg"></img>
                <EmblaCarousel type="jury" slides={SLIDES} options={OPTIONS} />
            </div>
        </div>
    );
}
