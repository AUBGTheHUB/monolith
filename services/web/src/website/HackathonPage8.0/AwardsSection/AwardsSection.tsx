export default function AwardsSection() {
    return (
        <div
            className="w-full flex flex-col items-center py-20 sm:py-32 relative bg-black before:absolute before:inset-0 before:bg-black before:opacity-50 before:z-0"
            style={{
                backgroundImage: "url('/AwardsSection/HackAUBG_8.0-Awards-Background.png')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
            }}
        >
            <div className="absolute left-8 sm:left-16 top-0 bottom-0 w-[8px] bg-white z-20"></div>
            <div className="absolute right-8 sm:right-16 top-0 bottom-0 w-[8px] bg-white z-20"></div>

            <div className="w-full flex items-center justify-center mb-28 sm:mb-36 relative z-30 px-8 sm:px-16">
                <div className="flex-1 h-[8px] bg-white"></div>
                <h2 className="text-white text-5xl sm:text-7xl font-orbitron font-bold tracking-[0.4em] mx-8 sm:mx-16 whitespace-nowrap">
                    AWARDS
                </h2>
                <div className="flex-1 h-[8px] bg-white"></div>
            </div>

            <div className="w-full flex justify-center relative z-10 mb-28 sm:mb-36">
                <div className="flex flex-col sm:flex-row items-center gap-12 sm:gap-20 px-8">
                    <div className="flex flex-col items-center w-full sm:w-auto order-2 sm:order-1">
                        <div className="relative rounded-[2rem] border-2 border-white overflow-hidden w-[400px] h-[625px] bg-orange-500 shadow-2xl flex flex-col">
                            <div className="pt-6 px-9 pb-5 flex items-center justify-center">
                                <p className="text-white text-4xl font-orbitron font-bold text-center">Second Place</p>
                            </div>
                            <div className="w-full h-[2px] bg-white"></div>
                            <div className="flex-1 flex items-center justify-center">
                                <p className="text-white text-[11rem] font-orbitron font-bold leading-none">2</p>
                            </div>
                            <div className="w-full h-[2px] bg-white"></div>
                            <div className="pt-5 pb-6 px-9 flex items-center justify-center">
                                <p className="text-white text-4xl font-orbitron font-bold text-center">2000 BGN</p>
                            </div>
                        </div>
                    </div>

                    <div className="flex flex-col items-center w-full sm:w-auto order-1 sm:order-2">
                        <div className="relative rounded-[2rem] border-2 border-white overflow-hidden w-[500px] h-[750px] bg-yellow-400 shadow-2xl flex flex-col">
                            <div className="pt-8 px-10 pb-6 flex items-center justify-center">
                                <p className="text-white text-6xl font-orbitron font-bold text-center">First Place</p>
                            </div>
                            <div className="w-full h-[2px] bg-white"></div>
                            <div className="flex-1 flex items-center justify-center">
                                <p className="text-white text-[14rem] font-orbitron font-bold leading-none">1</p>
                            </div>
                            <div className="w-full h-[2px] bg-white"></div>
                            <div className="pt-6 pb-8 px-10 flex items-center justify-center">
                                <p className="text-white text-6xl font-orbitron font-bold text-center">3000 BGN</p>
                            </div>
                        </div>
                    </div>

                    <div className="flex flex-col items-center w-full sm:w-auto order-3">
                        <div className="relative rounded-[2rem] border-2 border-white overflow-hidden w-[344px] h-[550px] bg-red-500 shadow-2xl flex flex-col">
                            <div className="pt-5 px-8 pb-4 flex items-center justify-center">
                                <p className="text-white text-3xl font-orbitron font-bold text-center">Third Place</p>
                            </div>
                            <div className="w-full h-[2px] bg-white"></div>
                            <div className="flex-1 flex items-center justify-center">
                                <p className="text-white text-[9.5rem] font-orbitron font-bold leading-none">3</p>
                            </div>
                            <div className="w-full h-[2px] bg-white"></div>
                            <div className="pt-4 pb-5 px-8 flex items-center justify-center">
                                <p className="text-white text-4xl font-orbitron font-bold text-center">1000 BGN</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="flex flex-col items-center w-full relative z-30">
                <div className="flex flex-col sm:flex-row justify-between items-start w-full text-white text-xl sm:text-2xl font-oxanium gap-8 sm:gap-16 mb-10 px-24 sm:px-48 leading-relaxed">
                    <div className="flex-1 text-left">
                        <p className="leading-relaxed">And much more!</p>
                        <p className="leading-relaxed">Take part in all of the games we have prepared!</p>
                    </div>
                    <div className="flex-1 text-left sm:text-right">
                        <p className="leading-relaxed">All participants will receive giftbags with</p>
                        <p className="leading-relaxed">swag from The Hub and all HackAUBG 6.0 partners!</p>
                    </div>
                </div>

                <div className="w-full flex items-center justify-center px-8 sm:px-16">
                    <div className="flex-1 h-[8px] bg-white"></div>
                    <div className="mx-12 sm:mx-16">
                        <img
                            src="/AwardsSection/HackAUBG_8.0-Awards-Logo.png"
                            alt="HackAUBG Logo"
                            className="w-12 h-12 sm:w-14 sm:h-14 object-contain"
                        />
                    </div>
                    <div className="flex-1 h-[8px] bg-white"></div>
                </div>
            </div>
        </div>
    );
}
