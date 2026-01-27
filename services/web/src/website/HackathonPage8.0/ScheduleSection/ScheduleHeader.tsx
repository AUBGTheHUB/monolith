export const ScheduleHeader = () => (
    <div
        className="flex items-center gap-4 lg:gap-6 mb-24 bg-white border-y-2 border-r-2 sm:border-2 border-black rounded-r-3xl px-6 lg:px-8 py-6 -ml-0 sm:-ml-8 mr-16 lg:mr-24 xl:mr-40"
        style={{ boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)' }}
    >
        <div className="ml-4 sm:ml-16 lg:ml-28 xl:ml-40 flex items-center gap-4 lg:gap-6">
            <img
                src="/ScheduleSection/logo.png"
                alt="HackAUBG Logo"
                className="w-10 h-10 sm:w-12 sm:h-12 lg:w-16 lg:h-16 object-contain"
            />
            <h2 className="text-black font-orbitron font-normal tracking-[0.3em] text-[clamp(1.25rem,3.5vw,3rem)]">
                SCHEDULE
            </h2>
        </div>
    </div>
);
