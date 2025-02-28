import { useState } from 'react';

interface FAQ {
    question: string;
    answer: string;
}

const faqs: FAQ[] = [
    {
        question: 'What is a hackathon?',
        answer: 'A hackathon is a design sprint-like event in which computer programmers and others involved in software development, including graphic designers, interface designers, project managers, domain experts, and others collaborate intensively on software projects.',
    },
    {
        question: 'Who can participate in the hackathon?',
        answer: "Anyone who is interested in coding, designing, or creating something new can participate in the hackathon. You don't need to be a professional developer to participate.",
    },
    {
        question: 'What are the prizes for the hackathon?',
        answer: 'The prizes for the hackathon are as follows: 1st Prize: $1000, 2nd Prize: $500, 3rd',
    },
    {
        question: 'What is a hackathon?',
        answer: 'A hackathon is a design sprint-like event in which computer programmers and others involved in software development, including graphic designers, interface designers, project managers, domain experts, and others collaborate intensively on software projects.',
    },
    {
        question: 'Who can participate in the hackathon?',
        answer: "Anyone who is interested in coding, designing, or creating something new can participate in the hackathon. You don't need to be a professional developer to participate.",
    },
    {
        question: 'What are the prizes for the hackathon?',
        answer: 'The prizes for the hackathon are as follows: 1st Prize: $1000, 2nd Prize: $500, 3rd',
    },
];

function FAQItem({
    id,
    faq,
    isOpen,
    setIsOpenFaqId,
}: {
    id: number;
    faq: FAQ;
    isOpen: boolean;
    setIsOpenFaqId: (id: number) => void;
}) {
    const handleClick = () => {
        if (isOpen) {
            setIsOpenFaqId(0);
        } else {
            setIsOpenFaqId(id);
        }
    };

    return (
        <div className="border-b border-[#233340] py-4 cursor-pointer" onClick={() => handleClick()}>
            <div className="flex justify-between">
                <div className="text-[#A9B4C3] flex items-center">
                    <p>{faq.question}</p>
                </div>
                <div className="cursor-pointer font-medium text-2xl text-[#009CF9]">
                    {isOpen && <span className="text-4xl select-none">-</span>}
                    {!isOpen && <span className="text-2xl select-none">+</span>}
                </div>
            </div>
            <div
                className={`${isOpen ? 'max-h-96' : 'max-h-0'} transition-[max-height] duration-700 ease-in-out overflow-hidden`}
            >
                {isOpen && (
                    <div className="pb-4">
                        <p>{faq.answer}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default function HackathonFAQSection() {
    const [isOpenFaqId, setIsOpenFaqID] = useState(0);

    return (
        <div className={`text-white sm:w-[80%] mx-6 sm:mx-auto pt-20`}>
            <div className="text-3xl sm:text-4xl flex items-center gap-4 mb-20">
                <img src="./n.png" alt="" className="w-[1.6rem]" />
                <h2>FAQ</h2>
            </div>
            <div
                style={{
                    minHeight: `${faqs.length * 65 + 120}px`,
                }}
            >
                {faqs.map((faq, index) => (
                    <FAQItem
                        key={index + 1}
                        id={index + 1}
                        faq={faq}
                        isOpen={isOpenFaqId === index + 1 ? true : false}
                        setIsOpenFaqId={setIsOpenFaqID}
                    />
                ))}
            </div>
        </div>
    );
}
