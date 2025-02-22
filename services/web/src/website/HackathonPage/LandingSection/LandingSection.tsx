import { useState, useEffect, Fragment } from 'react';

export default function LandingSection() {
    const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 768);

    useEffect(() => {
        const handleResize = () => {
            setIsDesktop(window.innerWidth >= 768);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return (
        <Fragment>
            {isDesktop ? (
                <div className="relative w-full h-[90%] pb-[40rem] sm:pb-[30rem] md:pb-[25rem] lg:pb-[20rem] xl:pb-[35rem] lg:b-[10rem] xs:pb-[35rem]">
                    <img className="w-full z-0" src="/public/hackLanding/space.svg"></img>
                    <img className="w-full z-0 block xl:hidden" src="/public/hackLanding/space.svg"></img>
                    <img className="w-full z-0 block xs:hidden" src="/public/hackLanding/space.svg"></img>
                    <img
                        className="lg:w-auto z-10 absolute z-0 lg:top-0 right-0 top-[20rem] w-1/2 "
                        src="/public/hackLanding/death_star.svg"
                    ></img>
                    <div className="w-full z-10 absolute lg:top-[11rem] md:top-[8rem] top-[6rem] inset-x-0 flex justify-center items-center">
                        <img className="lg:w-1/2 w-4/5 z-10" src="/public/hackLanding/title.svg"></img>
                    </div>
                </div>
            ) : (
                <div>
                    <div className="relative w-full h-[90%] ">
                        <img className="w-full z-0" src="/public/hackLanding/space.svg"></img>
                        <img className="w-full z-0 block xl:hidden" src="/public/hackLanding/space.svg"></img>
                        <img
                            className="lg:w-auto z-30 absolute z-0 lg:top-0 right-0 top-[20rem] w-1/2 "
                            src="/public/hackLanding/death_star.svg"
                        ></img>
                        <div className="w-full z-20 absolute lg:top-[11rem] md:top-[8rem] top-[6rem] inset-x-0 flex justify-center items-center">
                            <img className="lg:w-1/2 w-4/5 z-10" src="/public/hackLanding/title.svg"></img>
                        </div>
                        <div className="relative w-full min-h-[5rem]   bg-gradient-to-b from-stone-950/0 from-10% via-hackBg/50 via-25%  to-hackBg to-50% z-20 flex justify-center">
                            <img className="absolute top-[0rem] w-full z-10" src="/public/hackLanding/space.svg"></img>
                            <div className="w-4/5 relative lg:top-[11rem] top-[10rem] inset-x-0 z-20 flex-column ">
                                <div className="sm:text-4xl text-3xl sm:mb-5 mb-5 flex items-center ">
                                    <img src="./n.png" alt="" className="w-[1.6rem]" />
                                    <p className="text-white ml-5 tracking-[0.2em] font-normal">MISSION</p>
                                </div>
                                <div className=" text-mont text-[#A9B4C3] lg:py-20 py-10 sm:text-lg">
                                    <p>
                                        Over the course of 52 hours, you will work in teams to brainstorm and prototype
                                        your project idea based on the topic we will reveal during the Opening Ceremony,
                                        as well as pitch your project to a panel of judges. But you won’t be on your own
                                        - we will have a team of experienced mentors on hand to offer guidance and
                                        support throughout the event. Plus, there will be awesome prizes and food to
                                        keep you fueled and motivated!
                                    </p>
                                    <p className="pt-5 md:pt-2 md:pb-2 lg:pb-30 ">
                                        HackAUBG is more than just a hackathon - it’s a community of innovators,
                                        collaborators, and problem-solvers. We believe that together, we can create a
                                        better future through technology and creativity.
                                    </p>
                                </div>
                                <img
                                    className="w-full pb-[15rem] lg:pb-[30rem]"
                                    src="/public/hackMission/underline.svg"
                                ></img>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </Fragment>
    );
}
