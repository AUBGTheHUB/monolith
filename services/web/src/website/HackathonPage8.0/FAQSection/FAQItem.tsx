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
        if (contentRef.current) {
            setHeight(isOpen ? contentRef.current.scrollHeight : 0);
        }
    }, [isOpen]);

    return (
        <div className="relative">
            {/* Top separator */}
            <div className="h-px w-full bg-[#521010]" />

            {/* Question row */}
            <button
                onClick={onToggle}
                aria-expanded={isOpen}
                className="flex w-full items-center justify-between py-[19px] text-left"
            >
                <span className="font-oxanium text-[19px] leading-[100%] text-[#A9B4C3]">{faq.question}</span>

                {/* Icon container (LOCKED SIZE) */}
                <span className="relative h-[19px] w-[19px] flex items-center justify-center">
                    {/* PLUS */}
                    <img
                        src="/plus.svg"
                        alt="Expand answer"
                        className={`absolute h-[11px] w-[11px] transition-opacity duration-100 ${
                            isOpen ? 'opacity-0' : 'opacity-100'
                        }`}
                    />

                    {/* MINUS */}
                    <img
                        src="/minus.svg"
                        alt="Collapse answer"
                        className={`absolute h-[19px] w-[19px] transition-opacity duration-100 ${
                            isOpen ? 'opacity-100' : 'opacity-0'
                        }`}
                    />
                </span>
            </button>

            {/* Answer */}
            <div style={{ height }} className="overflow-hidden transition-[height] duration-300 ease-in-out">
                <div
                    ref={contentRef}
                    className="pt-[19px] pb-[19px] font-oxanium text-[19px] leading-[100%] text-[#FFFFFF]"
                >
                    {faq.answer}
                </div>
            </div>

            {/* Bottom separator */}
            <div className={`h-px w-full ${isOpen ? 'bg-[#DA2F2F]' : 'bg-[#521010]'}`} />
        </div>
    );
};
