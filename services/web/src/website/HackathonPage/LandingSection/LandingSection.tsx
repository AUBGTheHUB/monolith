export default function LandingSection() {
    // const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 768);

    // useEffect(() => {
    //     const handleResize = () => {
    //         setIsDesktop(window.innerWidth >= 768);
    //     };

    //     window.addEventListener('resize', handleResize);

    //     return () => {
    //         window.removeEventListener('resize', handleResize);
    //     };
    // }, []);

    return (
        <div
            className=" w-full h-auto lg:pb-[60rem] max-[1024px]:min-h-[100vh] pb-[30rem]   relative"
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
            <div className="w-full flex justify-center items-center min-h-[40vh] lg:min-h-[80vh]">
                <img className=" z-50 lg:w-1/2 w-[90%]" src="/hackLanding/title.svg" />
            </div>
            <div className=" w-full pt-[7rem] bg-gradient-to-b   z-20 flex justify-center">
                <div className="w-4/5 relative lg:top-[11rem] top-[10rem] inset-x-0 z-20 flex-column ">
                    <div className="sm:text-4xl text-3xl sm:mb-5 mb-5 flex items-center ">
                        <img src="./n.png" alt="" className="w-[1.6rem]" />
                        <p className="text-white ml-5 tracking-[0.2em] font-normal">MISSION</p>
                    </div>
                    <div className=" text-mont text-[#A9B4C3] lg:py-20 pt-10 pb-6 sm:text-lg">
                        <p>
                            Over the course of 52 hours, you will work in teams to brainstorm and prototype your project
                            idea based on the topic we will reveal during the Opening Ceremony, as well as pitch your
                            project to a panel of judges. But you won’t be on your own - we will have a team of
                            experienced mentors on hand to offer guidance and support throughout the event. Plus, there
                            will be awesome prizes and food to keep you fueled and motivated!
                        </p>
                        <p className="pt-5 md:pt-2 md:pb-2 lg:pb-30 ">
                            HackAUBG is more than just a hackathon - it’s a community of innovators, collaborators, and
                            problem-solvers. We believe that together, we can create a better future through technology
                            and creativity.
                        </p>
                    </div>
                    <img className="w-full z-50 pb-[15rem] lg:pb-[30rem]" src="/hackMission/underline.svg"></img>
                </div>
            </div>
        </div>
    );
}
