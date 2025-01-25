import HubberModule from './HubberModule';
import hubbers from '../StaticContent/hubbers.json';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/base.css';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/embla-team.css';
import EmblaCarousel from '@/components/EmblaCarousel/SlidesPerViewCarousel/js/EmblaCarousel.tsx';
import { EmblaOptionsType } from 'embla-carousel';
import React, { useState } from 'react';
import { Button } from '@/components/ui/button.tsx';

// Because the grid for the meet the team secion is 2x4
// each slide of the carousel is going to be of 2 elements above each other
// chunkArray splits the array of members into an array where each element consists of another array of 2 members
// which is then passed in order for the 2x4 grid carousel logic to work

// TO-DO: make api call for the actual pictures and hubbers information

function chunkArray(array: React.ReactElement[], chunkSize: number): React.ReactElement[][] {
    return array.reduce((resultArray, item, index) => {
        const chunkIndex = Math.floor(index / chunkSize);
        if (!resultArray[chunkIndex]) {
            resultArray[chunkIndex] = []; // Start a new chunk
        }
        resultArray[chunkIndex].push(item);
        return resultArray;
    }, [] as React.ReactElement[][]);
}

const OPTIONS: EmblaOptionsType = {
    slidesToScroll: 'auto',
    containScroll: 'trimSnaps',
};

export default function MeetTheTeamSection() {
    const [selected, setSelected] = useState('All');
    const handleSelect = (value: string) => {
        setSelected(value);
    };

    const initialSlides: React.ReactElement[] = hubbers
        .filter((hubbers) => hubbers.departments.includes(selected))
        .map((hubber, index) => <HubberModule imgSrc={hubber.picture} name={hubber.name} key={index} />);

    const SLIDES = chunkArray(initialSlides, 2);

    return (
        <div className="meet-team">
            <img
                src="/meetTheTeam/meet_the_team_blob.svg"
                className=" z-0 absolute blur-[10rem] h-[1490.43px] w-[1505.76px] top-[0rem] right-[-8rem] opacity-65 rotate-210 "
            ></img>
            <div className=" space-y-7 font-mont sm:w-3/5 w-11/12 mx-auto z-10 relative ">
                <h2 className="font-semibold text-3xl text-[#9cbeff] mb-10 ">Meet the team</h2>
                <div className="flex flex-wrap gap-3 ">
                    {['All', 'Board', 'PR', 'Design', 'Development', 'Marketing', 'Logistics'].map((label) =>
                        selected === label ? (
                            <Button
                                variant="team_selected"
                                size="round_sm"
                                className="font-semibold"
                                key={label}
                                onClick={() => handleSelect(label)}
                            >
                                {label}
                            </Button>
                        ) : (
                            <Button
                                variant="team"
                                size="round_sm"
                                className="font-semibold"
                                key={label}
                                onClick={() => handleSelect(label)}
                            >
                                {label}
                            </Button>
                        ),
                    )}
                </div>
                <EmblaCarousel type="team" slides={SLIDES} options={OPTIONS} />
            </div>
        </div>
    );
}
