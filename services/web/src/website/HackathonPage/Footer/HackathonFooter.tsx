const SECTIONS_CLASS_NAME = 'w-full md:w-1/2 lg:mr-8 lg:w-1/4 my-5 lg:my-0';
const SECTIONS_TITLE_CLASS_NAME = 'text-base my-4 select-none font-bold text-white';
const OPTIONS_CLASS_NAME = 'text-base my-4 text-[#E6E6E6]';
const LINKS_CLASS_NAME = 'hover:underline hover:text-white';

export const Footer = () => {
    return (
        <div className="relative flex flex-col font-mont">
            <div className="overflow-hidden relative flex w-full h-full bg-[#000912] justify-center py-20 flex-wrap z-10">
                <div className="flex flex-wrap lg:flex-nowrap mx-8 sm:w-[80%] sm:mx-0 z-10">
                    <div className={SECTIONS_CLASS_NAME}>
                        <h3 className={SECTIONS_TITLE_CLASS_NAME}>Links</h3>
                        <a href="/hackathon" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            Home
                        </a>
                        <a href="#mission" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            Mission
                        </a>
                        <a href="#journey" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            Journey
                        </a>
                        <a href="#mentors" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            Mentors/Jury
                        </a>
                        <a href="#schedule" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            Schedule
                        </a>
                        <a href="/" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            The Hub
                        </a>
                    </div>
                    <div className={SECTIONS_CLASS_NAME}>
                        <h3 className={SECTIONS_TITLE_CLASS_NAME}>Socials</h3>
                        <a
                            href="https://www.instagram.com/thehubaubg/"
                            className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}
                            target="_blank"
                            rel="noreferrer"
                        >
                            Instagram
                        </a>
                        <a
                            href="https://www.facebook.com/TheHubAUBG/"
                            className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}
                            target="_blank"
                            rel="noreferrer"
                        >
                            Facebook
                        </a>
                        <a
                            href="https://www.youtube.com/channel/UChdtBZBvaK9XZurP3GjPDug"
                            className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}
                            target="_blank"
                            rel="noreferrer"
                        >
                            Youtube
                        </a>
                    </div>
                    <div className={SECTIONS_CLASS_NAME}>
                        <h3 className={SECTIONS_TITLE_CLASS_NAME}>Address</h3>
                        <p className={OPTIONS_CLASS_NAME}>AUBG Blagoevgrad, Bulgaria</p>
                    </div>
                    <div className={SECTIONS_CLASS_NAME}>
                        <h3 className={SECTIONS_TITLE_CLASS_NAME}>Contact</h3>
                        <a href="mailto:thehubaubg@gmail.com" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            thehubaubg@gmail.com
                        </a>
                    </div>
                </div>
                <span className="mt-2 mx-8 w-full sm:w-[80%] sm:mx-0 h-[1px] bg-[#4D4D4D]" />
                <div className="w-full mx-8 sm:mx-0 sm:w-[80%]">
                    <p className="text-[#B4B4B4] text-sm mt-2">Copyright TheHub 2025</p>
                </div>
            </div>
        </div>
    );
};
