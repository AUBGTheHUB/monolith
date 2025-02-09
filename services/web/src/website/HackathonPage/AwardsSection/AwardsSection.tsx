export default function AwardsSection() {
    return (
        <div className="w-full flex flex-col items-center font-mont bg-[#000912] py-10">
            <div className="w-4/5 flex items-start mt-10">
                <img src="./n.png" alt="" className="w-[1.6rem] mt-3" />
                <p className="text-white ml-5 tracking-[0.2em] text-3xl sm:text-4xl">AWARDS</p>
            </div>

            <div className="flex flex-row justify-center min-h-[600px] items-center w-[100%]  space-x-20">
                <img src="/AwardsSection/awards_bg.png" className="absolute h-[160vh] right-[26vh] mt-[-2rem] w-auto" />
                <div className="flex flex-col items-center">
                    <img
                        src="/AwardsSection/blue_stone.png"
                        alt=""
                        className="h-[5.8rem] w-[3.2rem] mr-[3.2rem]  mb-4"
                    />
                    <div className="flex items-end">
                        <p className=" font-bold text-5xl bg-gradient-to-b from-[#00DCFF] to-[#CBE1FF] text-transparent bg-clip-text">
                            2000
                        </p>
                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>
                <div className="flex flex-col items-center mb-[4.2rem]">
                    <img src="/AwardsSection/red_stone.png" alt="" className="h-[10rem] w-[5.5rem] mr-[3.2rem] mb-4" />
                    <div className="flex items-end">
                        <p className="  font-bold text-5xl bg-gradient-to-b from-[#FE4646] to-[#A9B4C3] text-transparent bg-clip-text">
                            3000
                        </p>

                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>
                <div className="flex flex-col items-center mt-[1rem]">
                    <img src="/AwardsSection/white_stone.png" alt="" className="h-[5rem] w-[3rem] mr-[3.2rem]  mb-4" />
                    <div className="flex items-end">
                        <p className=" font-bold text-5xl bg-gradient-to-b from-[#CBE1FF] to-[#A9B4C3] text-transparent bg-clip-text">
                            1000
                        </p>

                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>
            </div>

            <div className="flex flex-col w-3/5 text-[#A9B4C3] text-sm">
                <hr className="" />
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
