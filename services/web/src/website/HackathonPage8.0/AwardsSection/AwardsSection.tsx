export default function AwardsSection() {
    return (
        <section
            className="w-full flex flex-col items-center py-12 lg:py-20 xl:py-32 relative bg-black before:absolute before:inset-0 before:bg-black before:opacity-70 before:z-0 rounded-t-lg"
            style={{
                backgroundImage: "url('/AwardsSection/HackAUBG_8.0-Awards-Background.png')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
            }}
        >
            <div className="absolute left-4 lg:left-8 xl:left-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-white z-20"></div>
            <div className="absolute right-4 lg:right-8 xl:right-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-white z-20"></div>

            <div className="w-full flex items-center justify-center mb-16 lg:mb-24 xl:mb-36 relative z-30 px-4 lg:px-8 xl:px-16">
                <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true"></div>
                <h2 className="text-white text-3xl lg:text-5xl xl:text-7xl font-orbitron font-bold tracking-[0.4em] mx-4 lg:mx-8 xl:mx-16 whitespace-nowrap">
                    AWARDS
                </h2>
                <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true"></div>
            </div>

            <div className="w-full flex justify-center relative z-10 mb-16 lg:mb-24 xl:mb-36">
                <div className="flex flex-col lg:flex-row items-center gap-8 lg:gap-[3vw] xl:gap-20 xl:mr-[75px] px-4">
                    <article className="flex flex-col items-center w-full lg:w-auto">
                        <div className="relative rounded-[1.5rem] lg:rounded-[2rem] border-2 border-white overflow-hidden w-[240px] lg:w-[25vw] xl:w-[400px] h-[380px] lg:h-[40vw] xl:h-[625px] bg-[url('/AwardsSection/2nd.png')] bg-cover bg-center bg-no-repeat shadow-2xl flex flex-col">
                            <div className="pt-4 lg:pt-[1vw] xl:pt-6 px-6 lg:px-[1.5vw] xl:px-9 pb-3 lg:pb-[0.8vw] xl:pb-5 flex items-center justify-center border-b-[2px] border-white">
                                <h3 className="text-white text-xl lg:text-[2vw] xl:text-4xl font-orbitron font-bold text-center">
                                    Second Place
                                </h3>
                            </div>

                            <div className="flex-1 flex items-center justify-center">
                                <p className="text-white text-[6rem] lg:text-[7vw] xl:text-[11rem] font-orbitron font-bold leading-none">
                                    2
                                </p>
                            </div>

                            <div className="pt-3 lg:pt-[0.8vw] xl:pt-5 pb-4 lg:pb-[1vw] xl:pb-6 px-6 lg:px-[1.5vw] xl:px-9 flex items-center justify-center border-t-[2px] border-white">
                                <p className="text-white text-xl lg:text-[2vw] xl:text-4xl font-orbitron font-bold text-center">
                                    2000 BGN
                                </p>
                            </div>
                        </div>
                    </article>

                    <article className="flex flex-col items-center w-full lg:w-auto">
                        <div className="relative rounded-[1.5rem] lg:rounded-[2rem] border-2 border-white overflow-hidden w-[280px] lg:w-[32vw] xl:w-[500px] h-[440px] lg:h-[48vw] xl:h-[750px] bg-[url('/AwardsSection/1st.png')] bg-cover bg-center bg-no-repeat shadow-2xl flex flex-col">
                            <div className="pt-5 lg:pt-[1.2vw] xl:pt-8 px-6 lg:px-[2vw] xl:px-10 pb-4 lg:pb-[1vw] xl:pb-6 flex items-center justify-center border-b-[2px] border-white">
                                <h3 className="text-white text-2xl lg:text-[3.5vw] xl:text-6xl font-orbitron font-bold text-center">
                                    First Place
                                </h3>
                            </div>

                            <div className="flex-1 flex items-center justify-center">
                                <p className="text-white text-[8rem] lg:text-[9vw] xl:text-[14rem] font-orbitron font-bold leading-none">
                                    1
                                </p>
                            </div>

                            <div className="pt-4 lg:pt-[1vw] xl:pt-6 pb-5 lg:pb-[1.2vw] xl:pb-8 px-6 lg:px-[2vw] xl:px-10 flex items-center justify-center border-t-[2px] border-white">
                                <p className="text-white text-2xl lg:text-[3.5vw] xl:text-6xl font-orbitron font-bold text-center">
                                    3000 BGN
                                </p>
                            </div>
                        </div>
                    </article>

                    <article className="flex flex-col items-center w-full lg:w-auto">
                        <div className="relative rounded-[1.5rem] lg:rounded-[2rem] border-2 border-white overflow-hidden w-[200px] lg:w-[22vw] xl:w-[344px] h-[320px] lg:h-[35vw] xl:h-[550px] bg-[url('/AwardsSection/3rd.png')] bg-cover bg-center bg-no-repeat shadow-2xl flex flex-col">
                            <div className="pt-3 lg:pt-[0.8vw] xl:pt-5 px-4 lg:px-[1.2vw] xl:px-8 pb-2 lg:pb-[0.6vw] xl:pb-4 flex items-center justify-center border-b-[2px] border-white">
                                <h3 className="text-white text-lg lg:text-[1.8vw] xl:text-3xl font-orbitron font-bold text-center">
                                    Third Place
                                </h3>
                            </div>

                            <div className="flex-1 flex items-center justify-center">
                                <p className="text-white text-[5rem] lg:text-[6vw] xl:text-[9.5rem] font-orbitron font-bold leading-none">
                                    3
                                </p>
                            </div>

                            <div className="pt-2 lg:pt-[0.6vw] xl:pt-4 pb-3 lg:pb-[0.8vw] xl:pb-5 px-4 lg:px-[1.2vw] xl:px-8 flex items-center justify-center border-t-[2px] border-white">
                                <p className="text-white text-xl lg:text-[2vw] xl:text-4xl font-orbitron font-bold text-center">
                                    1000 BGN
                                </p>
                            </div>
                        </div>
                    </article>
                </div>
            </div>

            <div className="flex flex-col items-center w-full relative z-30">
                <div className="flex flex-col lg:flex-row justify-between items-start w-full text-white text-base lg:text-[1.2vw] xl:text-2xl font-oxanium gap-6 lg:gap-8 xl:gap-16 mb-8 lg:mb-10 px-8 lg:px-[4vw] xl:px-32 leading-relaxed">
                    <div className="flex-1 text-left">
                        <p className="leading-relaxed">And much more!</p>
                        <p className="leading-relaxed">Take part in all of the games we have prepared!</p>
                    </div>
                    <div className="flex-1 text-left lg:text-right">
                        <p className="leading-relaxed">
                            All participants will receive giftbags with swag from The Hub and all HackAUBG 8.0 partners!
                        </p>
                    </div>
                </div>

                <div className="w-full flex items-center justify-center px-4 lg:px-8 xl:px-16">
                    <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true"></div>
                    <div className="mx-6 lg:mx-[2vw] xl:mx-16">
                        <img
                            src="/AwardsSection/HackAUBG_8.0-Awards-Logo.png"
                            alt="HackAUBG Logo"
                            className="w-10 h-10 lg:w-[2.5vw] lg:h-[2.5vw] xl:w-14 xl:h-14 object-contain"
                        />
                    </div>
                    <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true"></div>
                </div>
            </div>
        </section>
    );
}
