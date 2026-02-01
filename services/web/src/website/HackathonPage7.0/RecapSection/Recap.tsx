export const Recap = () => {
    return (
        <div className="relative w-full flex justify-center items-center font-mont bg-[#000912]">
            <div className="relative w-full lg:py-20 pb-20">
                <div className="absolute sm:top-16 md:top-20 right-0 opacity-70 bg-[url('/orbits-recap-background.webp')] bg-cover bg-no-repeat bg-[position:right_-5vw_top] h-[50vw] max-h-[600px] w-[50vw] max-w-[600px]" />
                <div className="w-[80%] mx-auto  relative">
                    <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center w-4/5">
                        <img src="./n.webp" alt="" className="w-[1.6rem]" />
                        <p className="text-white ml-5 tracking-[0.2em] ">TRAILER</p>
                    </div>
                    <div className="relative rounded-lg overflow-hidden bg-black/20">
                        <iframe
                            className="video"
                            width="100%"
                            height="750px"
                            src={'https://www.youtube.com/embed/UAE_0mkBYi0?si=cK_Jg0drEen2K2Wt'}
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            title="Embedded youtube"
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};
