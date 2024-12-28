const SECTIONS_CLASS_NAME = 'w-full sm:w-1/2 lg:mx-14 lg:w-1/4 my-5 lg:my-0';
const SECTIONS_TITLE_CLASS_NAME = 'text-base my-2 select-none font-bold text-white';
const OPTIONS_CLASS_NAME = 'text-base my-2 text-[#E6E6E6]';
const LINKS_CLASS_NAME = 'hover:underline';

export const Footer = () => {
    return (
        <div className="flex w-full h-full bg-gradient-to-t from-[#0B2340] via-[#1A344F] to-[#1E4D5D] justify-center py-20">
            <div className="flex flex-wrap lg:flex-nowrap w-[60%]">
                <div className={SECTIONS_CLASS_NAME}>
                    <h3 className={SECTIONS_TITLE_CLASS_NAME}>Address</h3>
                    <p className={OPTIONS_CLASS_NAME}>AUBG Blagoevgrad, Bulgaria</p>
                </div>
                <div className={SECTIONS_CLASS_NAME}>
                    <h3 className={SECTIONS_TITLE_CLASS_NAME}>Links</h3>
                    <a href="#home" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                        Home
                    </a>
                    <a href="#about-us" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                        About us
                    </a>
                    <a href="#events" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                        Events
                    </a>
                    <a href="#meet-the-team" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                        The team
                    </a>
                    <a href="#hackAUBG" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                        HackAUBG
                    </a>
                </div>
                <div className={SECTIONS_CLASS_NAME}>
                    <h3 className={SECTIONS_TITLE_CLASS_NAME}>Socials</h3>
                    <a
                        href="https://www.instagram.com/thehubaubg/"
                        className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}
                    >
                        Instagram
                    </a>
                    <a href="" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                        Facebook
                    </a>
                    <a href="" className={`${OPTIONS_CLASS_NAME} ${LINKS_CLASS_NAME}`}>
                        Youtube
                    </a>
                </div>
                <div className={SECTIONS_CLASS_NAME}>
                    <h3 className={SECTIONS_TITLE_CLASS_NAME}>Contact</h3>
                    <p className={OPTIONS_CLASS_NAME}>thehub@aubg.edu</p>
                </div>
            </div>
        </div>
    );
};
