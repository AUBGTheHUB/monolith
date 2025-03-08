import MissionSection from '../MissionSection/MissionSection';

export default function LandingSection() {
    return (
        <div
            className=" w-full h-auto lg:pb-[45rem] max-[1024px]:min-h-[100vh] pb-[55rem] relative"
            style={{
                backgroundImage: 'url("/verifyPage/background.png")',
                backgroundSize: 'cover',
                backgroundPosition: 'right',
                backgroundRepeat: 'repeat',
            }}
        >
            <img
                className="lg:w-auto absolute z-10 lg:top-0 right-0 top-[25rem] w-[70%]"
                src="/hackLanding/death_star.svg"
            />
            <div className="w-full flex justify-center  min-h-[100vh] lg:min-h-[80vh]">
                <div className="flex justify-center max-[1024px]:items-start max-[1024px]:mt-[5rem] w-full">
                    <img className="flex z-50 lg:w-1/2 w-[90%]" src="/hackLanding/title.svg" />
                </div>
            </div>
            <MissionSection />
        </div>
    );
}
