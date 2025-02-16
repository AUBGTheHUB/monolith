export default function AwardsSection() {
    return (
        <div
            className="w-full flex flex-col items-center font-mont bg-[#000912] sm:py-10 relative"
            style={{
                backgroundImage: "url('/AwardsSection/awards_bg.png')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
            }}
        >
            <div className="w-4/5 flex items-start mb-32">
                <img src="./n.png" alt="" className="w-[1.6rem] mt-3" />
                <p className="text-white ml-5 tracking-[0.2em] text-3xl sm:text-4xl">AWARDS</p>
            </div>
            <div className="flex flex-col sm:flex-row justify-center items-center w-[100%] space-x-0 sm:space-x-16 space-y-20 sm:space-y-0 mb-32 relative">
                <div className="flex flex-col items-center">
                    <img
                        src="/AwardsSection/blue_stone.png"
                        alt=""
                        className="w-[19vw] sm:w-[4vw] mr-0 sm:mr-[3.2rem] mb-4"
                    />
                    <div className="flex items-end">
                        <p className="font-bold text-7xl sm:text-6xl bg-gradient-to-b from-[#00DCFF] to-[#CBE1FF] text-transparent bg-clip-text">
                            2000
                        </p>
                        <p className="text-white text-lg mb-1 ml-2">BGN</p>
                    </div>
                </div>
                <div className="flex flex-col items-center z-10 !mb-16">
                    <img
                        src="/AwardsSection/red_stone.png"
                        alt=""
                        className="w-[21vw] sm:w-[6vw] mr-0 sm:mr-[3.5rem] mb-[1.2rem]"
                    />
                    <div className="flex items-end">
                        <p className="font-bold  text-8xl sm:text-7xl bg-gradient-to-b from-[#FE4646] to-[#A9B4C3] text-transparent bg-clip-text">
                            3000
                        </p>
                        <p className="text-white text-lg ml-2 mb-1">BGN</p>
                    </div>
                </div>
                <div className="flex flex-col items-center !mt-0 sm:!mt-2 ">
                    <img
                        src="/AwardsSection/white_stone.png"
                        alt=""
                        className="w-[17vw] sm:w-[3.5vw] mr-0 sm:mr-[3.2rem] mb-4"
                    />
                    <div className="flex items-end">
                        <p className="font-bold text-7xl sm:text-6xl bg-gradient-to-b from-[#9daec6] to-[#c8d0dc] text-transparent bg-clip-text">
                            1000
                        </p>
                        <p className="text-white text-lg ml-2 mb-[0.1rem]">BGN</p>
                    </div>
                </div>
            </div>
            <div className="flex flex-col w-11/12 sm:w-3/5 text-[#A9B4C3] text-sm relative z-10">
                <img src="/AwardsSection/line.svg" alt="Divider" className="w-full h-auto" />
                <div className="mt-10 flex flex-col gap-y-4">
                    <div className="flex items-start w-full">
                        <span className="w-5 h-[2px] bg-[#009CF9] flex-shrink-0 mr-4 mt-[0.55rem]"></span>
                        <span className="w-full break-words">And much more!</span>
                    </div>

                    <div className="flex items-start w-full">
                        <span className="w-5 h-[2px] bg-[#009CF9] flex-shrink-0 mr-4 mt-[0.55rem]"></span>
                        <span className="w-full break-words">Take part in all of the games we have prepared!</span>
                    </div>

                    <div className="flex items-start w-full">
                        <span className="w-5 h-[2px] bg-[#009CF9] flex-shrink-0 mr-4 mt-[0.55rem]"></span>
                        <span className="w-full break-words">
                            All participants will receive gift bags with swag from The Hub and all HackAUBG 6.0
                            partners!
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}
