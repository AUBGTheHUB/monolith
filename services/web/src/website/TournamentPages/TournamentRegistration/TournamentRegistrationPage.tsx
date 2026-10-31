import ellipse1 from './images/ellipse1.png';
import line from './images/line.png';
import diamond from './images/diamond.png';

import { useEffect, useState } from 'react';
import TournamentRegistrationForm from './TournamentRegistrationForm.tsx';

import {
    formFrameStyles,
    glowStyles,
    sectionStyles,
    subtitleStyles,
    titleGoldStyles,
    titleStyles,
    titleWhiteStyles,
} from './styles.ts';

export default function RegistrationFormPage() {
    const [fadeIn, setFadeIn] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setFadeIn(true), 100);
        return () => clearTimeout(timer);
    }, []);

    return (
        <section id="register" className={`${sectionStyles} ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
            <div className={glowStyles} />

            <img
                src={ellipse1}
                alt=""
                className="pointer-events-none absolute left-1/2 top-0 z-10 h-auto w-[min(95vw,1400px)] max-w-none -translate-x-1/2"
            />

            <div className="z-10 flex items-center justify-center gap-[clamp(12px,2.5vw,40px)] mt-[clamp(4rem,14vw,11rem)] mb-[clamp(1rem,2vw,2rem)]">
                <img src={line} alt="" className="pointer-events-none h-auto w-[clamp(48px,17vw,200px)] shrink-0" />
                <img src={diamond} alt="" className="pointer-events-none h-auto w-[clamp(18px,3.5vw,48px)] shrink-0" />
                <img
                    src={line}
                    alt=""
                    className="pointer-events-none h-auto w-[clamp(48px,17vw,200px)] shrink-0 rotate-180"
                />
            </div>

            <h2 className={titleStyles}>
                <span className={titleWhiteStyles}>TOURNAMENT</span>
                <br />
                <span className={titleGoldStyles}>REGISTRATION</span>
            </h2>

            <p className={subtitleStyles}>Fill in the form below to register for the tournament</p>

            <div className={formFrameStyles}>
                <TournamentRegistrationForm />
            </div>
        </section>
    );
}
