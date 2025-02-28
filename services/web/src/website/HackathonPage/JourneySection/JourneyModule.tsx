type JourneyModule = {
    title: string;
    text: string;
};

function JourneyModule({ title, text }: JourneyModule) {
    return (
        <div className="scroll-section text-white">
            <div className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] w-[100vh] relative">
                <div className="absolute left-[0.30rem] top-[20%] w-1 h-24 bg-white rounded-lg -translate-x-2"></div>
                <h3 className="text-white text-xl mb-2">{title}</h3>
                <p className="text-[#A9B4C3] md:text-md text-xs">{text}</p>
                <div className="absolute right-6 bottom-0 flex gap-2 translate-y-1/2">
                    <div className="w-2 h-2 rounded-full bg-white"></div>
                    <div className="w-2 h-2 rounded-full bg-white"></div>
                    <div className="w-2 h-2 rounded-full bg-white"></div>
                </div>
            </div>
        </div>
    );
}

export default JourneyModule;
