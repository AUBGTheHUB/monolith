import React from 'react';
import { Award } from './awardsConfig';

export const AwardCard: React.FC<Award> = ({ title, prize, currency, number, image }) => {
    // Removed max constraints so cards can scale properly with vh/vw
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
            w: 'w-[280px] lg:w-[20vw] xl:w-[20vw]',
            h: 'h-[440px] lg:h-[55vh] xl:h-[55vh]',
            fontNumber: 'text-[8rem] lg:text-[12vh] xl:text-[12vh]',
            fontPrize: 'text-2xl lg:text-[3vh] xl:text-[3vh]',
            fontTitle: 'text-2xl lg:text-[3vh] xl:text-[3vh]',
        },
        2: {
            w: 'w-[240px] lg:w-[16vw] xl:w-[16vw]',
            h: 'h-[380px] lg:h-[46vh] xl:h-[46vh]',
            fontNumber: 'text-[6rem] lg:text-[10vh] xl:text-[10vh]',
            fontPrize: 'text-xl lg:text-[2.5vh] xl:text-[2.5vh]',
            fontTitle: 'text-xl lg:text-[2.3vh] xl:text-[2.3vh]',
        },
        3: {
            w: 'w-[200px] lg:w-[14vw] xl:w-[14vw]',
            h: 'h-[320px] lg:h-[40vh] xl:h-[40vh]',
            fontNumber: 'text-[5rem] lg:text-[8vh] xl:text-[8vh]',
            fontPrize: 'text-lg lg:text-[2vh] xl:text-[2vh]',
            fontTitle: 'text-lg lg:text-[1.8vh] xl:text-[1.8vh]',
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
                    <h3 className={`text-white font-orbitron font-bold text-center ${classes.fontTitle}`}>{title}</h3>
                </div>

                <div className="flex-1 flex items-center justify-center">
                    <p className={`text-white font-orbitron font-bold leading-none ${classes.fontNumber}`}>{number}</p>
                </div>

                <div className="flex items-center justify-center border-t-[2px] border-white px-6 lg:px-[2vw] pt-3 lg:pt-[1vh] pb-4 lg:pb-[1.5vh]">
                    <p className={`text-white font-orbitron font-bold text-center ${classes.fontPrize}`}>
                        <span className="award-amount">{prize}</span>{' '}
                        <span className="award-currency-unit">{currency}</span>
                    </p>
                </div>
            </div>
        </article>
    );
};
