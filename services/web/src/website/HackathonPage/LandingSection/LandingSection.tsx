export default function LandingSection() {
    return (
        <div className="relative w-full pb-[15rem] md:pb-[8rem] lg:pb-[20rem] xl:pb-[12rem] lg:b-[10rem]">
            <img className="w-full z-0" src="/public/hackLanding/space.svg"></img>
            <img className="w-auto z-10 absolute z-0 top-0 right-0" src="/public/hackLanding/death_star.svg"></img>
            <div className="w-full  z-10 absolute lg:top-[11rem] md:top-[8rem] top-[3rem] inset-x-0 flex justify-center items-center">
                <img className="lg:w-auto w-1/2 z-10" src="/public/hackLanding/title.svg"></img>
            </div>
        </div>
    );
}
