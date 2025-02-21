export default function LandingSection() {
    return (
        <div className="relative w-full pb-[20rem] md:pb-[20rem] lg:pb-[20rem] xl:pb-[12rem] lg:b-[10rem]">
            <img className="w-full z-0" src="/public/hackLanding/space.svg"></img>
            <img className="w-full z-0 block sm:hidden" src="/public/hackLanding/space.svg"></img>
            <img className="w-full z-0 block sm:hidden" src="/public/hackLanding/space.svg"></img>
            <img
                className="md:w-auto z-10 absolute z-0 md:top-0 right-0 top-[20rem] w-1/2 "
                src="/public/hackLanding/death_star.svg"
            ></img>
            <div className="w-full z-10 absolute lg:top-[11rem] md:top-[8rem] top-[6rem] inset-x-0 flex justify-center items-center">
                <img className="lg:w-auto w-5/8 z-10" src="/public/hackLanding/title.svg"></img>
            </div>
        </div>
    );
}
