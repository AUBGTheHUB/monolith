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
            <div className="w-full flex items-center justify-center mb-24 sm:mb-32 px-8 relative z-10">
                <div className="flex-1 h-[2px] bg-white"></div>
                <h2 className="text-white text-4xl sm:text-6xl font-orbitron font-normal tracking-[0.4em] mx-8 sm:mx-16 whitespace-nowrap">
                    AWARDS
                </h2>
                <div className="flex-1 h-[2px] bg-white"></div>
            </div>

            <div className="flex flex-col sm:flex-row justify-center items-end w-full max-w-7xl px-8 mb-24 sm:mb-32 gap-8 sm:gap-16 relative z-10">
                <div className="flex flex-col items-center w-full sm:w-auto order-2 sm:order-1 sm:mb-12">
                    <div className="relative rounded-[2rem] border-2 border-white overflow-hidden w-[280px] h-[420px] bg-orange-500 shadow-2xl">
                        <div className="relative z-10 flex flex-col items-start justify-between h-full p-8">
                            <p className="text-white text-xl sm:text-2xl font-orbitron font-normal">Second Place</p>
                            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                                <p className="text-white text-[10rem] sm:text-[12rem] font-orbitron font-bold leading-none">
                                    2
                                </p>
                            </div>
                            <div className="self-start mt-auto">
                                <p className="text-white text-4xl sm:text-5xl font-orbitron font-bold">2000 BGN</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col items-center w-full sm:w-auto order-1 sm:order-2">
                    <div className="relative rounded-[2rem] border-2 border-white overflow-hidden w-[320px] h-[480px] bg-yellow-400 shadow-2xl">
                        <div className="relative z-10 flex flex-col items-start justify-between h-full p-8">
                            <p className="text-white text-xl sm:text-2xl font-orbitron font-normal">First Place</p>
                            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                                <p className="text-white text-[12rem] sm:text-[14rem] font-orbitron font-bold leading-none">
                                    1
                                </p>
                            </div>
                            <div className="self-start mt-auto">
                                <p className="text-white text-5xl sm:text-6xl font-orbitron font-bold">3000 BGN</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col items-center w-full sm:w-auto order-3 sm:mb-12">
                    <div className="relative rounded-[2rem] border-2 border-white overflow-hidden w-[280px] h-[420px] bg-red-500 shadow-2xl">
                        <div className="relative z-10 flex flex-col items-start justify-between h-full p-8">
                            <p className="text-white text-xl sm:text-2xl font-orbitron font-normal">Third Place</p>
                            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                                <p className="text-white text-[10rem] sm:text-[12rem] font-orbitron font-bold leading-none">
                                    3
                                </p>
                            </div>
                            <div className="self-start mt-auto">
                                <p className="text-white text-4xl sm:text-5xl font-orbitron font-bold">1000 BGN</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="flex flex-col items-center w-11/12 sm:w-4/5 max-w-6xl relative z-10">
                <div className="w-full h-[2px] bg-white mb-12"></div>

                <div className="flex flex-col sm:flex-row justify-between items-start w-full text-white text-base sm:text-lg font-oxanium gap-8 sm:gap-16 mb-12">
                    <div className="flex-1 text-left">
                        <p className="mb-3">And much more!</p>
                        <p>Take part in all of the games we have prepared!</p>
                    </div>
                    <div className="flex-1 text-left sm:text-right">
                        <p>
                            All participants will receive giftbags with swag from The Hub and all HackAUBG 6.0 partners!
                        </p>
                    </div>
                </div>

                <div className="mb-8">
                    <img
                        src="/AwardsSection/HackAUBG_8.0-Awards-Logo.png"
                        alt="HackAUBG Logo"
                        className="w-16 h-16 sm:w-20 sm:h-20 object-contain"
                    />
                </div>
            </div>
        </div>
    );
}
