export default function AwardsSection() {
    return (
        <div className="w-full flex flex-col items-center font-mont bg-[#000912] py-10">
            <div className="w-4/5 flex items-start mb-10">
                <img src="./n.png" alt="" className="w-[1.6rem]" />
                <p className="text-white ml-5 tracking-[0.2em] text-3xl sm:text-4xl">AWARDS</p>
            </div>

            <div className="flex flex-row justify-center items-center space-x-16 w-3/5">
                <div className="flex flex-col items-center">
                    <img src="/AwardsSection/blue_stone.png" alt="" className="h-[5.8rem] w-[3.2rem]" />
                    <div className="flex">
                        <p className="text-white text-5xl">2000</p>
                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>
                <div className="flex flex-col items-center">
                    <img src="/AwardsSection/red_stone.png" alt="" className="h-[10rem] w-[5.5rem]" />
                    <div className="flex">
                        <p className="text-white text-7xl">3000</p>
                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>
                <div className="flex flex-col items-center">
                    <img src="/AwardsSection/white_stone.png" alt="" className="h-[5.8rem] w-[3.2rem]" />
                    <div className="flex">
                        <p className="text-white text-5xl">1000</p>
                        <p className="text-white text-lg ml-2">BGN</p>
                    </div>
                </div>
            </div>

            <div className="flex flex-col items-center mt-8 w-3/5 text-center text-white space-y-2">
                <hr className="" />
                <p>And much more!</p>
                <p>Take part in all of the games we have prepared!</p>
                <p>All participants will receive giftbags with swag from The Hub and all HackAUBG 6.0 partners!</p>
            </div>
        </div>
    );
}
