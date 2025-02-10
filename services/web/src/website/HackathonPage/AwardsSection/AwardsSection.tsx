export default function AwardsSection() {
    return (
        <div
            className="w-full flex flex-col items-center font-mont bg-[#000912] py-10 relative"
            style={{
                backgroundImage: "url('/AwardsSection/awards_bg.png')",
                backgroundSize: '180vh',
                backgroundPosition: 'center top -30vh',
                backgroundRepeat: 'no-repeat',
            }}
        >
            <div className="w-4/5 flex items-start mt-10 mb-28">
                <img src="./n.png" alt="" className="w-[1.6rem] mt-3" />
                <p className="text-white ml-5 tracking-[0.2em] text-3xl sm:text-4xl">AWARDS</p>
            </div>

            {/* Centered Container */}
            <div className="flex flex-row justify-center items-center w-[100%] space-x-16 mb-28 relative">
                {/* Left */}
                <div className="flex flex-col items-center">
                    <img src="/AwardsSection/blue_stone.png" alt="" className="vw-20 mr-[3.2rem] mb-4" />
                    <div className="flex items-end">
                        <p className="font-bold text-6xl bg-gradient-to-b from-[#00DCFF] to-[#CBE1FF] text-transparent bg-clip-text">
                            2000
                        </p>
                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>

                {/* Middle - Adjust to Center */}
                <div className="flex flex-col items-center mb-[3.4rem] relative z-10">
                    <img src="/AwardsSection/red_stone.png" alt="" className="vw-25 mr-[3.5rem] mb-4" />
                    <div className="flex items-end">
                        <p className="font-bold text-7xl bg-gradient-to-b from-[#FE4646] to-[#A9B4C3] text-transparent bg-clip-text">
                            3000
                        </p>
                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>

                {/* Right */}
                <div className="flex flex-col items-center mt-[1rem]">
                    <img src="/AwardsSection/white_stone.png" alt="" className="vw-20 mr-[3.2rem] mb-4" />
                    <div className="flex items-end">
                        <p className="font-bold text-6xl bg-gradient-to-b from-[#CBE1FF] to-[#A9B4C3] text-transparent bg-clip-text">
                            1000
                        </p>
                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>
            </div>

            {/* Bottom Section */}
            <div className="flex flex-col w-3/5 text-[#A9B4C3] text-sm relative z-10">
                <img src="/AwardsSection/line.svg" alt="Divider" className="w-full h-auto" />
                <div className="mt-10 flex flex-col flex-start">
                    <div className="mb-2 flex items-center before:content-[''] before:inline-block before:w-5 before:h-[2px] before:bg-[#009CF9] before:mr-4">
                        <span>And much more!</span>
                    </div>
                    <div className="mb-2 flex items-center before:content-[''] before:inline-block before:w-5 before:h-[2px] before:bg-[#009CF9] before:mr-4">
                        <span>Take part in all of the games we have prepared!</span>
                    </div>
                    <div className="mb-2 flex items-center before:content-[''] before:inline-block before:w-5 before:h-[2px] before:bg-[#009CF9] before:mr-4">
                        <span>
                            All participants will receive giftbags with swag from The Hub and all HackAUBG 6.0 partners!
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}
