import { useEffect, useRef, useState } from 'react';
import type { FaqItem } from './types';

type Props = {
    faq: FaqItem;
    isOpen: boolean;
    onToggle: () => void;
};

export const FAQItem = ({ faq, isOpen, onToggle }: Props) => {
    const contentRef = useRef<HTMLDivElement>(null);
    const [height, setHeight] = useState(0);

    useEffect(() => {
        const updateHeight = () => {
            if (contentRef.current) {
                setHeight(isOpen ? contentRef.current.scrollHeight : 0);
            }
        };
        updateHeight();
        window.addEventListener('resize', updateHeight);
        return () => window.removeEventListener('resize', updateHeight);
    }, [isOpen]);

    return (
        <div className="relative border-b border-[#521010]">
            <button
                onClick={onToggle}
                aria-expanded={isOpen}
                className="flex w-full items-center justify-between py-5 text-left group"
            >
                {/* TEXT FIX: Scales smoothly between 16px and 20px depending on screen width */}
                <span className="font-oxanium text-[clamp(16px,1.5vw,20px)] leading-tight text-[#A9B4C3] group-hover:text-white transition-colors">
                    {faq.question}
                </span>

                <span className="relative flex h-6 w-6 flex-shrink-0 items-center justify-center ml-4">
                    <img
                        src="/plus.svg"
                        alt="Expand"
                        className={`absolute h-3 w-3 transition-transform duration-200 ${isOpen ? 'rotate-90 opacity-0' : 'opacity-100'}`}
                    />
                    <img
                        src="/minus.svg"
                        alt="Collapse"
                        className={`absolute h-3 w-auto transition-transform duration-200 ${isOpen ? 'opacity-100' : '-rotate-90 opacity-0'}`}
                    />
                </span>
            </button>

            <div style={{ height }} className="overflow-hidden transition-[height] duration-300 ease-in-out">
                <div
                    ref={contentRef}
                    // TEXT FIX: Same smooth scaling for the answer
                    className="pb-6 pt-2 font-oxanium text-[clamp(16px,1.5vw,19px)] leading-relaxed text-[#FFFFFF] opacity-90"
                >
                    {faq.answer}
                </div>
            </div>
        </div>
    );
};
