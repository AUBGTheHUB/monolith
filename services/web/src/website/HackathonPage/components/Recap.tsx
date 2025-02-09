export const Recap = () => {
    return (
        <div className="relative w-full py-36">
            <div
                className="absolute sm:top-16 md:top-20 right-0 w-1/12 h-full opacity-70"
                style={{
                    backgroundImage: 'url("/orbits-recap-background.png")',
                    backgroundSize: 'cover',
                    backgroundPosition: `right -${5}vw top`,
                    backgroundRepeat: 'no-repeat',
                    height: "50vw",
                    maxHeight: "600px",
                    width: "50vw",
                    maxWidth: "600px"
                }}
            />
            <div className="max-w-7xl mx-auto px-12 relative">
                <div className="flex items-center gap-3 mb-24">
                    <img src="/yellow-n-icon.svg" alt="N icon" className="w-6 h-6" />
                    <h1 className="font-mont text-white text-3xl mb">RECAP</h1>
                </div>
                <div className="relative rounded-lg overflow-hidden bg-black/20">
                    <video
                        className="w-full rounded-lg aspect-[16/7] object-cover"
                        controls
                        autoPlay
                        muted
                        playsInline
                    >
                        {/* TODO: change the big buck bunnny video with the actual recap... */}
                        <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>
        </div>
    )
}
