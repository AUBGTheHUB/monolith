import React from 'react';
import { GradingCategory } from './types';

const CriteriaRow = ({ label, points }: { label: string; points: number }) => (
    <div className="flex justify-between items-center py-3 lg:py-[1.5vh] border-b border-white/20 shadow-[0_5px_10px_-7px_rgba(0,0,0,0.3)]">
        <span className="text-white font-oxanium text-sm lg:text-[1.8vh] leading-tight pr-4">{label}</span>
        <span className="text-white font-oxanium font-bold text-sm lg:text-[1.8vh]">{points}</span>
    </div>
);

type GradingCardProps = {
    left: GradingCategory;
    right: GradingCategory;
    isDarkTop?: boolean; // for da style as per the design on the figma
};

export const GradingCard: React.FC<GradingCardProps> = ({ left, right, isDarkTop = false }) => {
    const gradientClass = isDarkTop
        ? 'bg-gradient-to-bl from-[#AA1515] via-[#EF5A1A] to-[#FA9E28]'
        : 'bg-gradient-to-bl from-[#FA9E28] via-[#EF5A1A] to-[#AA1515]';

    return (
        <div className={`w-full rounded-[2rem] shadow-2xl p-8 lg:p-[3vh] overflow-hidden ${gradientClass}`}>
            <div className="flex flex-col lg:flex-row gap-8 lg:gap-[4vw]">
                <div className="flex-1">
                    <div className="flex justify-between items-center pb-5 ">
                        <h3 className="text-white font-orbitron font-bold text-sm lg:text-[2vh] tracking-wider uppercase">
                            {left.title}
                        </h3>
                        <span className="text-white font-orbitron font-bold text-sm lg:text-[2vh]">Points</span>
                    </div>
                    <div>
                        {left.items.map((item, idx) => (
                            <CriteriaRow key={idx} label={item.label} points={item.points} />
                        ))}
                    </div>
                </div>

                <div className="flex-1">
                    <div className="flex justify-between items-center pb-5 ">
                        <h3 className="text-white font-orbitron font-bold text-sm lg:text-[2vh] tracking-wider uppercase">
                            {right.title}
                        </h3>
                        <span className="text-white font-orbitron font-bold text-sm lg:text-[2vh]">Points</span>
                    </div>
                    <div>
                        {right.items.map((item, idx) => (
                            <CriteriaRow key={idx} label={item.label} points={item.points} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};
