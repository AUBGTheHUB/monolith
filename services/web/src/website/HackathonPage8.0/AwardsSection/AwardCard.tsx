import React from 'react';
import { Award } from './awardsConfig';

export const AwardCard: React.FC<Award> = ({ title, prize, currency, number, image }) => {
    const classMap: Record<
        number,
        {
            w: string;
            h: string;
            fontNumber: string;
            fontPrize: string;
            fontTitle: string;
        }
    > = {
        1: {
            w: 'w-[280px] lg:w-[22vw] xl:w-[22vw]',
            h: 'h-[440px] lg:h-[55vh] xl:h-[55vh]',
            fontNumber: 'text-[8rem] lg:text-[min(14vh,14vw)] xl:text-[min(14vh,14vw)]',
            fontPrize: 'text-2xl lg:text-[min(4vh,4.5vw)] xl:text-[min(4vh,4.5vw)]',
            fontTitle: 'text-2xl lg:text-[min(4vh,4.5vw)] xl:text-[min(4vh,4.5vw)]',
        },
        2: {
            w: 'w-[240px] lg:w-[18vw] xl:w-[18vw]',
            h: 'h-[380px] lg:h-[46vh] xl:h-[46vh]',
            fontNumber: 'text-[6rem] lg:text-[min(11vh,12vw)] xl:text-[min(11vh,12vw)]',
            fontPrize: 'text-xl lg:text-[min(3.2vh,3.5vw)] xl:text-[min(3.2vh,3.5vw)]',
            fontTitle: 'text-xl lg:text-[min(3vh,3.2vw)] xl:text-[min(3vh,3.2vw)]',
        },
        3: {
            w: 'w-[200px] lg:w-[16vw] xl:w-[16vw]',
            h: 'h-[320px] lg:h-[40vh] xl:h-[40vh]',
            fontNumber: 'text-[5rem] lg:text-[min(9.5vh,10vw)] xl:text-[min(9.5vh,10vw)]',
            fontPrize: 'text-lg lg:text-[min(2.6vh,3vw)] xl:text-[min(2.6vh,3vw)]',
            fontTitle: 'text-lg lg:text-[min(2.4vh,2.7vw)] xl:text-[min(2.4vh,2.7vw)]',
        },
    };

    const classes = classMap[number];

    return (
        <article className="flex flex-col items-center w-full lg:w-auto">
            <div
                className={`relative rounded-[1.5rem] lg:rounded-[2rem] border-2 border-white overflow-hidden shadow-2xl flex flex-col ${classes.w} ${classes.h}`}
            >
                <img
                    src={image}
                    alt={`${title} award background`}
                    className="absolute inset-0 w-full h-full object-cover -z-10"
                />

                <div className="flex items-center justify-center border-b-[2px] border-white px-6 lg:px-[2vw] pt-4 lg:pt-[1.5vh] pb-3 lg:pb-[1vh]">
                    <h3
                        className={`text-white font-orbitron font-bold text-center leading-relaxed ${classes.fontTitle}`}
                    >
                        {title}
                    </h3>
                </div>

                <div className="flex-1 flex items-center justify-center">
                    <p className={`text-white font-orbitron font-bold leading-none ${classes.fontNumber}`}>{number}</p>
                </div>

                <div className="flex items-center justify-center border-t-[2px] border-white px-6 lg:px-[2vw] pt-3 lg:pt-[1vh] pb-4 lg:pb-[1.5vh]">
                    <p
                        className={`text-white font-orbitron font-bold text-center leading-relaxed ${classes.fontPrize}`}
                    >
                        <span className="award-amount">{prize}</span>{' '}
                        <span className="award-currency-unit">{currency}</span>
                    </p>
                </div>
            </div>
        </article>
    );
};
