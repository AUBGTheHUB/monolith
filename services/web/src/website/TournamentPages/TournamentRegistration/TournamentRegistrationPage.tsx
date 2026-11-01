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
import { useFeatureSwitches } from '@/config.ts';

export default function RegistrationFormPage() {
    const featureSwitches = useFeatureSwitches();
    const [fadeIn, setFadeIn] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setFadeIn(true), 100);
        return () => clearTimeout(timer);
    }, []);

    return (
        <>
            <section id="register" className={`${sectionStyles} ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
                <div className={glowStyles} />
                <div className="pointer-events-none absolute left-0 top-[min(19vw,260px)] z-0 h-[min(47vw,640px)] -translate-x-[68%]">
                    <img
                        src="/Tournament/hextech.png"
                        alt="Hextech"
                        className="h-full w-auto max-w-none animate-spin object-contain [animation-duration:60s]"
                    />
                </div>

                <div className="relative z-10 aspect-[1000/73] w-[min(78vw,850px)] overflow-hidden">
                    <div className="absolute bottom-0 left-1/2 aspect-square w-[350%] -translate-x-1/2 rounded-full border-2 border-[#C79B3B]" />
                </div>

                <div className="relative z-10 mt-[clamp(0.5rem,1.8vw,1.75rem)] flex w-fit flex-col items-center">
                    <div className="mb-[clamp(0.75rem,1.6vw,1.5rem)] flex w-0 min-w-full items-center gap-[clamp(10px,1.8vw,28px)]">
                        <div className="h-[2px] flex-1 bg-[#C79B3B]" />
                        <img
                            src="/Tournament/diamond.png"
                            alt=""
                            className="pointer-events-none h-auto w-[clamp(18px,3.5vw,48px)] shrink-0"
                        />
                        <div className="h-[2px] flex-1 bg-[#C79B3B]" />
                    </div>

                    <h2 className={`${titleStyles} !w-auto !px-0`}>
                        <span className={titleWhiteStyles}>TOURNAMENT</span>
                        <br />
                        <span className={titleGoldStyles}>REGISTRATION</span>
                    </h2>
                </div>

                {featureSwitches.RegSwitch && (
                    <>
                        <p className={subtitleStyles}>Fill in the form below to register for the tournament</p>
                        <div className={formFrameStyles}>
                            <TournamentRegistrationForm isRegTeamsFull={featureSwitches.isRegTeamsFull} />
                        </div>
                    </>
                )}
                {!featureSwitches.RegSwitch && <p className={subtitleStyles}>Registration closed</p>}
            </section>
        </>
    );
}
