export default function MissionSection() {
    return (
        <div className="absolute xxl:top-[50girem] xl:top-[30rem]  xs:top-[20rem] lg:top-[35rem] md:top-[50rem] sm:top-[30rem] top-[19rem] w-full lg:min-h-[50rem] min-h-[5rem] pt-[4rem]  bg-gradient-to-b from-stone-950/0 from-10% via-hackBg/50 via-25%  to-hackBg to-50% z-20 flex justify-center">
            <div className="w-4/5 relative lg:top-[11rem] top-[5rem] inset-x-0  flex-column ">
                <div className="sm:text-4xl text-3xl sm:mb-5 mb-5 flex items-center ">
                    <img src="./n.png" alt="" className="w-[1.6rem]" />
                    <p className="text-white ml-5 tracking-[0.2em] font-normal">MISSION</p>
                </div>
                <div className=" text-mont text-[#A9B4C3] lg:py-20 py-10 lg:text-[20px] text-[10px] md:text-[15px]">
                    <p>
                        Over the course of 52 hours, you will work in teams to brainstorm and prototype your project
                        idea based on the topic we will reveal during the Opening Ceremony, as well as pitch your
                        project to a panel of judges. But you won’t be on your own - we will have a team of experienced
                        mentors on hand to offer guidance and support throughout the event. Plus, there will be awesome
                        prizes and food to keep you fueled and motivated!
                    </p>
                    <p className="pt-10 md:pt-2 md:pb-2 lg:pb-30 ">
                        HackAUBG is more than just a hackathon - it’s a community of innovators, collaborators, and
                        problem-solvers. We believe that together, we can create a better future through technology and
                        creativity.
                    </p>
                </div>
                <img className="w-full pb-80 lg:pb-[30rem]" src="/public/hackMission/underline.svg"></img>
            </div>
        </div>
    );
}
