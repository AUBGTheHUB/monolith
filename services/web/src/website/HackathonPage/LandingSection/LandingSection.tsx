export default function LandingSection() {
    return (
        <div className="relative w-full h-[90%] pb-[40rem] sm:pb-[30rem] md:pb-[25rem] lg:pb-[20rem] xl:pb-[25rem] lg:b-[10rem] xs:pb-[35rem]">
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
    );
}
