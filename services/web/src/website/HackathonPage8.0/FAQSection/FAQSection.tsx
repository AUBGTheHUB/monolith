    import { useState } from 'react';
    import { FAQItem } from './FAQItem';
    import { faqs } from './data';
    import { VerticalBar } from '@/components/ui/verticalBar.tsx';

    export const FAQSection = () => {
        const [openFaqId, setOpenFaqId] = useState<number | null>(null);

        return (
            <section id="faq" className="relative w-full min-h-screen:dvh rounded-[20px] overflow-hidden bg-[#151313]">
                {/* Background image */}
                <div
                    className="absolute inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25] z-0"
                    style={{ backgroundImage: "url('/rocksBG.png')" }}
                />

                <VerticalBar isRight={true} isBlack={false} />
                <VerticalBar isRight={false} isBlack={false} />
                {/* Content */}
                <div className="relative z-10 mx-auto max-w-[1200px] px-6 md:px-20 py-12">
                    <div className="flex items-center gap-3 md:gap-[5px]">
                        <img src="/yellow_icon.svg" alt="FAQ icon" className="h-8 md:h-[42px] w-auto" />
                        <h2 className="font-orbitron text-2xl md:text-4xl lg:text-[40px] leading-tight text-[#FFFDF5]">FAQ</h2>
                    </div>

                    <div className="mt-12 md:mt-24 w-full h-auto">
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
