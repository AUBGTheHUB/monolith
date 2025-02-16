export default function JourneySection() {
    //TODO: change the journey steps titles and descriptions to the actual ones/
    const journeySteps = [
        {
            title: "1. Present and Win",
            description: "This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!",
            position: "left-[-0.17rem] top-[20%]",
            dotPosition: "right-6 bottom-0 translate-y-1/2"
        },
        {
            title: "2. Present and Win",
            description: "This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!",
            position: "right-[-0.17rem] top-[30%]",
            dotPosition: "left-6 bottom-0 translate-y-1/2"
        },
        {
            title: "3. Present and Win",
            description: "This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!",
            position: "left-[-0.17rem] bottom-[20%]",
            dotPosition: "right-6 top-0 -translate-y-1/2"
        }
    ];

    return (
        <div className="relative w-full flex justify-center items-center font-mont bg-[#000912]">
            <div className="relative w-4/5 flex flex-col z-10 my-24">
                <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center ">
                    <img src="./n.png" alt="" className="w-[1.6rem]" />
                    <p className="text-white ml-5 tracking-[0.2em]">JOURNEY</p>
                </div>
                <div className="flex flex-wrap justify-between gap-x-[calc((100%-3*30%)/2)] gap-y-6">
                    {journeySteps.map((step, index) => (
                        <div key={index} className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] relative w-full sm:w-[100%] lg:w-[30%]">
                            <div className={`absolute ${step.position} w-1 h-24 bg-white rounded-lg`}></div>
                            <h3 className="text-white text-lg mb-2">{step.title}</h3>
                            <p className="text-[#A9B4C3] text-xs">{step.description}</p>
                            <div className={`absolute ${step.dotPosition} flex gap-2`}>
                                <div className="w-2 h-2 rounded-full bg-white"></div>
                                <div className="w-2 h-2 rounded-full bg-white"></div>
                                <div className="w-2 h-2 rounded-full bg-white"></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}
