import { useEffect, useRef, useState } from 'react';

type FaqItem = {
    id: number;
    question: string;
    answer: string;
};

const LOREM =
    'Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,molestiae quas vel sint commodi repudiandae consequuntur.';

const faqs: FaqItem[] = [
    { id: 1, question: 'When does the registration start and end?', answer: LOREM },
    { id: 2, question: 'Are there any age restrictions for participants?', answer: LOREM },
    { id: 3, question: 'Who can I contact for more information?', answer: LOREM },
    { id: 4, question: 'What are the eligibility criteria for registration?', answer: LOREM },
    { id: 5, question: 'Where can I find the registration form?', answer: LOREM },
    { id: 6, question: 'Is there a registration fee?', answer: LOREM },
    { id: 7, question: 'Can I register online?', answer: LOREM },
    { id: 8, question: 'What documents do I need to submit?', answer: LOREM },
    { id: 9, question: 'Who can I contact for more information?', answer: LOREM },
];

type FAQItemProps = {
    faq: FaqItem;
    isOpen: boolean;
    onToggle: () => void;
};

const FAQItem = ({ faq, isOpen, onToggle }: FAQItemProps) => {
    const contentRef = useRef<HTMLDivElement>(null);
    const [height, setHeight] = useState(0);

    useEffect(() => {
        if (contentRef.current) {
            setHeight(isOpen ? contentRef.current.scrollHeight : 0);
        }
    }, [isOpen]);

    return (
        <div className="relative">
            {/* Top separator — always visible */}
            <div className="h-px w-full bg-[#521010]" />

            {/* Question row */}
            <button onClick={onToggle} className="flex w-full items-center justify-between py-[19px] text-left">
                <span className="text-[18px] text-[#A9B4C3]">{faq.question}</span>

                {/* Plus / Minus */}
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

            {/* Answer (expanded spacing matches Figma) */}
            <div style={{ height }} className="overflow-hidden transition-[height] duration-300 ease-in-out">
                <div ref={contentRef} className="pt-[19px] pb-[19px] text-[16px] text-[#FFFDF5]">
                    {faq.answer}
                </div>
            </div>

            {/* Bottom separator — active when open */}
            <div className={`h-px w-full ${isOpen ? 'bg-[#DA2F2F]' : 'bg-[#521010]'}`} />
        </div>
    );
};

export const FAQSection = () => {
    const [openFaqId, setOpenFaqId] = useState<number | null>(null);

    return (
        <section id="faq" className="relative w-full bg-[#151313] py-32 overflow-hidden">
            {/* Background image with blur + drop shadow */}
            <div
                className="absolute inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25] shadow-[0_4px_4px_rgba(0,0,0,0.25)]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            <div className="relative z-10 mx-auto max-w-[1400px] px-8">
                {/* Header */}
                <div className="flex items-center gap-4">
                    <img src="/yellow_icon.svg" alt="FAQ icon" className="h-[42px] w-auto" />
                    <h2 className="font-orbitron text-[40px] text-[#FFFDF5]">FAQ</h2>
                </div>

                {/* FAQ list */}
                <div className="mt-16">
                    {faqs.map((faq) => (
                        <FAQItem
                            key={faq.id}
                            faq={faq}
                            isOpen={openFaqId === faq.id}
                            onToggle={() => setOpenFaqId(openFaqId === faq.id ? null : faq.id)}
                        />
                    ))}
                </div>
            </div>
        </section>
    );
};
