import HubberModule from './HubberModule';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/base.css';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/embla-team.css';
import EmblaCarousel from '@/components/EmblaCarousel/SlidesPerViewCarousel/js/EmblaCarousel.tsx';
import { EmblaOptionsType } from 'embla-carousel';
import React, { useState } from 'react';
import { Button } from '@/components/ui/button.tsx';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient';
import { Departments, type BaseHubMember } from '@/types/hub-member';

// Because the grid for the meet the team secion is 2x4
// each slide of the carousel is going to be of 2 elements above each other
// chunkArray splits the array of members into an array where each element consists of another array of 2 members
// which is then passed in order for the 2x4 grid carousel logic to work
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
    const [selected, setSelected] = useState<Departments>(Departments.All);
    const [carouselKey, setCarouselKey] = useState(0);

    const { data: hubbers } = useQuery({
        queryKey: ['meet-the-team', 'get', 'hub-members'],
        queryFn: () => apiClient.get<{ members: BaseHubMember[] }>('/admin/hub-members'),
        select: (data) => data.members,
    });

    const handleSelect = (value: Departments) => {
        setSelected(value);
        setCarouselKey((prevKey) => prevKey + 1);
    };

    const initialSlides: React.ReactElement[] = hubbers
        ? hubbers
              .filter((hubbers) => {
                  if (selected === Departments.All) return true;
                  return hubbers.departments.includes(selected);
              })
              .map((hubber, index) => <HubberModule imgSrc={hubber.avatar_url} name={hubber.name} key={index} />)
        : [];

    const SLIDES = chunkArray(initialSlides, 2);

    return (
        <div className="meet-team">
            <img
                src="https://hubarskibucket.s3.eu-central-1.amazonaws.com/the-hub-2025/website-elements/gradient-meet-the-team.webp"
                alt="a gradient"
                className="z-0 absolute h-[2190.43px] top-[4rem] pointer-events-none w-full"
            />
            <div className="space-y-7 font-mont sm:w-3/5 w-11/12 mx-auto z-10 relative">
                <h2 className="font-semibold text-3xl text-[#9cbeff] mb-10">Meet the team</h2>
                <div className="flex flex-wrap gap-3">
                    {Object.values(Departments).map((label) =>
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
                <EmblaCarousel key={carouselKey} type="team" slides={SLIDES} options={OPTIONS} />
            </div>
        </div>
    );
}
