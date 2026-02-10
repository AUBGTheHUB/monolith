import redPin from './assets/red-pin.svg';
import yellowPin from './assets/yellow-pin.svg';
import { Carousel } from './components/Caroussel';

export const MentorsAndJudgesSection = () => {
    return (
        <section
            style={{
                backgroundImage: "url('/rocksBG.png')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
                backgroundColor: 'rgba(0,0,0,0.5)', // apply 0.5 opacity without affecting child elements
                backgroundBlendMode: 'overlay',
            }}
            className="text-white w-full py-28 rounded-[20px] overflow-hidden flex flex-col items-center justify-center gap-[100px]"
        >
            <Carousel title="MENTORS" imgSrc={yellowPin} />

            <Carousel title="JUDGES" imgSrc={redPin} />
        </section>
    );
};
