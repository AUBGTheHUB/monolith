// import hextech from './images/hextech.png';
import ellipse1 from './images/ellipse1.png';
import line from './images/line.png';
import diamond from './images/diamond.png';

import { useEffect, useState } from 'react';
import TournamentRegistrationForm from './TournamentRegistrationForm.tsx';

import { titleStyles, sectionStyles, titleWhiteStyles, titleGoldStyles } from './styles.ts';

export default function RegistrationFormPage() {
    const [fadeIn, setFadeIn] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setFadeIn(true), 100);
        return () => clearTimeout(timer);
    }, []);

    return (
        <section id="register" className={`${sectionStyles} ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
            {/* <img src={hextech} alt="" className={gearStyles} /> */}
            <img
                src={ellipse1}
                alt=""
                className="pointer-events-none absolute left-1/2 -translate-x-1/2 top-0 z-10 w-[95%] md:w-[85%] lg:w-[75%]"
            />
            <div className="z-10 flex items-center justify-center gap-5 md:gap-8 lg:gap-10 mt-16 md:mt-24 lg:mt-[170px] mb-6 md:mb-8 lg:mb-10">
                <img src={line} alt="" className="pointer-events-none w-20 md:w-40 lg:w-[218px]" />
                <img src={diamond} alt="" className="pointer-events-none w-[40px] md:w-[52px] lg:w-[63px]" />
                <img src={line} alt="" className="pointer-events-none w-20 md:w-40 lg:w-[218px] rotate-180" />
            </div>

            <h2 className={titleStyles}>
                <span className={titleWhiteStyles}>TOURNAMENT</span>
                <br />
                <span className={titleGoldStyles}>REGISTRATION</span>
            </h2>

            <p className="font-['Rubik'] font-light text-lg sm:text-xl md:text-[28px] lg:text-[36px] leading-[1.19] text-[#90D5FF] text-center w-full max-w-[892px] px-4 mb-6 md:mb-8 z-10">
                Fill in the form below to register for the tournament
            </p>
            <div className="relative z-10 w-11/12 max-w-[820px] overflow-hidden bg-[#C79B3B] p-2 md:p-3">
                <TournamentRegistrationForm />
            </div>
        </section>
    );
}
