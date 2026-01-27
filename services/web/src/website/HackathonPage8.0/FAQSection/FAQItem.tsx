import { useEffect, useRef, useState } from 'react';
import type { FaqItem } from './FAQ.types';

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
            <div className="h-px w-full bg-[#521010]" />

            <button
                onClick={onToggle}
                aria-expanded={isOpen}
                className="flex w-full items-center justify-between py-[19px] text-left"
            >
                <span className="font-oxanium text-[19px] leading-[100%] text-[#A9B4C3]">{faq.question}</span>

                <span className="flex items-center justify-center select-none">
                    {isOpen ? (
                        <span className="block h-[1px] w-[19px] bg-[#DA2F2F]" />
                    ) : (
                        <span className="relative block h-[11px] w-[11px]">
                            <span className="absolute inset-x-0 top-1/2 h-[1px] bg-[#DA2F2F]" />
                            <span className="absolute inset-y-0 left-1/2 w-[1px] bg-[#DA2F2F]" />
                        </span>
                    )}
                </span>
            </button>

            <div style={{ height }} className="overflow-hidden transition-[height] duration-300 ease-in-out">
                <div
                    ref={contentRef}
                    className="pt-[19px] pb-[19px] font-oxanium text-[19px] leading-[100%] text-[#FFFFFF]"
                >
                    {faq.answer}
                </div>
            </div>

            <div className={`h-px w-full ${isOpen ? 'bg-[#DA2F2F]' : 'bg-[#521010]'}`} />
        </div>
    );
};
