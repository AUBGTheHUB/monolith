const SECTIONS_CLASS_NAME = 'w-full md:w-1/2 lg:mr-8 lg:w-1/4 my-5 lg:my-0';
const SECTIONS_TITLE_CLASS_NAME = 'text-base my-4 select-none font-bold text-white';
const OPTIONS_CLASS_NAME = 'text-base my-4 text-[#E6E6E6]';
const LINKS_CLASS_NAME = 'hover:underline hover:text-white';

export const Footer = () => {
    return (
        <div className="relative flex flex-col" id="footer">
            <div className="overflow-hidden relative flex w-full h-full bg-gradient-to-t to-[#0B2340] from-[#0a1320] justify-center py-20 flex-wrap z-10">
                <img
                    src="/footer/footer-gradient.png"
                    className="absolute h-[70rem] top-[-50rem] right-[-15rem] pointer-events-none w-screen"
                />
                <div className="flex flex-wrap lg:flex-nowrap w-full mx-8 sm:w-[60%] sm:mx-0 z-10">
                    <div className={SECTIONS_CLASS_NAME}>
                        <h3 className={SECTIONS_TITLE_CLASS_NAME}>Links</h3>
                        <a href="/" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            Home
                        </a>
                        <a href="#about-us" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            About us
                        </a>
                        <a href="#past-events" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            Events
                        </a>
                        <a href="#meet-team" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            The team
                        </a>
                        <a href="/hackathon" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                            HackAUBG
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
                        <a
                            href="https://www.linkedin.com/company/the-hub-aubg/"
                            className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}
                            target="_blank"
                            rel="noreferrer"
                        >
                            Linkedin
                        </a>
                    </div>
                    <div className={SECTIONS_CLASS_NAME}>
                        <h3 className={SECTIONS_TITLE_CLASS_NAME}>Address</h3>
                        <p className={OPTIONS_CLASS_NAME}>AUBG Blagoevgrad, Bulgaria</p>
                    </div>
                    <div className={SECTIONS_CLASS_NAME}>
                        <h3 className={SECTIONS_TITLE_CLASS_NAME}>Contact</h3>
                        <p className={OPTIONS_CLASS_NAME}>
                            <a className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`} href="mailto:thehub@aubg.edu">
                                thehub@aubg.edu
                            </a>
                        </p>
                    </div>
                </div>
                <span className="mt-2 w-full mx-8 sm:mx-0 sm:w-[60%] h-[1px] bg-[#4D4D4D]" />
                <div className="w-full mx-8 sm:mx-0 sm:w-[60%]">
                    <p className="text-[#B4B4B4] text-sm mt-2">Copyright TheHub 2025</p>
                </div>
            </div>
        </div>
    );
};
