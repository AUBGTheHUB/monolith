import { useState } from 'react';
import { FAQItem } from './FAQItem';
import { faqs } from './faq.data';

export const FAQSection = () => {
    const [openFaqId, setOpenFaqId] = useState<number | null>(null);

    return (
        <section id="faq" className="relative w-full py-32 rounded-[20px] overflow-hidden bg-[#151313]">
            {/* Background image */}
            <div
                className="absolute inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            {/* LEFT vertical line */}
            <div className="pointer-events-none absolute top-0 bottom-0 left-[39px] w-[7px] bg-[#FFFDF5] hidden md:block" />

            {/* RIGHT vertical line */}
            <div className="pointer-events-none absolute top-0 bottom-0 right-[39px] w-[7px] bg-[#FFFDF5] hidden md:block" />

            {/* Content */}
            <div className="relative z-10 mx-auto max-w-[1400px] px-8">
                <div className="flex items-center gap-[5px]">
                    <img src="/yellow_icon.svg" alt="FAQ icon" className="h-[42px] w-auto" />
                    <h2 className="font-orbitron text-[40px] leading-[100%] text-[#FFFDF5]">FAQ</h2>
                </div>

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
