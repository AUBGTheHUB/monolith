import { useState } from 'react';
import { FAQItem } from './FAQItem';
import { faqs } from './data';
import { SectionTitle } from '../shared/SectionTitle';

export const FAQSection = () => {
    const [openFaqId, setOpenFaqId] = useState<number | null>(null);

    return (
        <section id="faq" className="relative w-full py-28 overflow-hidden bg-[#151313]">
            {/* Background image */}
            <div
                className="absolute inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            {/* Content */}
            <div
                className="relative z-10 w-full mx-auto px-8 md:px-0"
                style={{ maxWidth: 'clamp(40rem, 82vw, 80rem)' }}
            >
                <SectionTitle title="FAQ" iconSrc="/yellow_icon.svg" iconAlt="FAQ icon" dark />

                <div className="pt-20">
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
