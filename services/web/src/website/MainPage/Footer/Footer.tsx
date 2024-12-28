const SECTIONS_CLASS_NAME = 'w-full md:w-1/2 lg:mx-8 lg:w-1/4 my-5 lg:my-0';
const SECTIONS_TITLE_CLASS_NAME = 'text-base my-4 select-none font-bold text-white';
const OPTIONS_CLASS_NAME = 'text-base my-4 text-[#E6E6E6]';
const LINKS_CLASS_NAME = 'hover:underline';
import blob from '../../../../public/footer/footer_blob.svg';

export const Footer = () => {
    return (
        <div className="flex w-full h-full bg-gradient-to-t to-[#0B2340] from-[#0a1320] justify-center py-20 flex-wrap">
            <img src={blob} className="blur-[12.5rem] absolute overflow-hidden h-[35rem] top-[-22.5rem] right-[7rem]" />

            <div className="flex flex-wrap lg:flex-nowrap w-[60%]">
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
                    <h3 className={SECTIONS_TITLE_CLASS_NAME}>Address</h3>
                    <p className={OPTIONS_CLASS_NAME}>AUBG Blagoevgrad, Bulgaria</p>
                </div>
                <div className={SECTIONS_CLASS_NAME}>
                    <h3 className={SECTIONS_TITLE_CLASS_NAME}>Contact</h3>
                    <p className={OPTIONS_CLASS_NAME}>thehub@aubg.edu</p>
                </div>
            </div>
            <span className="mt-2 w-[57vw] h-[1px] bg-[#4D4D4D]" />
            <div className="w-[57%]">
                <p className="text-[#B4B4B4] text-sm mt-2">Copyright TheHub 2025</p>
            </div>
        </div>
    );
};
