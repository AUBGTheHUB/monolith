import { useState, useRef, useEffect } from 'react';

interface FAQ {
    question: string;
    answer: string;
}

const faqs: FAQ[] = [
    {
        question: 'I want to participate! When is the deadline for registering?',
        answer: 'Registration is open until Friday, March 21st.',
    },
    {
        question: 'How many people can be in a team?',
        answer: 'The minimum number of people in a team is 4, but you can have up to 6 people in a team. The ideal team would consist of one or two software developers, a designer, and one or two business planners. Keep in mind that if your team is with less than 4 people we will have to place more people in your team',
    },
    {
        question: 'Can I register without a team?',
        answer: 'Of course! If you are alone or if you only have 1 other teammate, you can register and a facilitator from the Hub’s organizing team will help you in finding more teammates.',
    },
    {
        question: 'Where will the Hackathon be held?',
        answer: 'The Hackathon will be in American University in Bulgaria’s ABF Sports Hall, located on ul. Svoboda Bachvarova 12 in Blagoevgrad.',
    },
    {
        question: 'How much time will we have to develop our projects?',
        answer: 'The brainstorming process starts on Friday at 21:00 and you will have until Sunday at 12:00 to submit your project. Make sure you keep an eye on the clock!',
    },
    {
        question: 'Is there a topic for the Hackathon?',
        answer: 'Yes! However, it will be kept a secret until the Opening Ceremony on Friday.',
    },
    {
        question: 'Can I start developing something in advance?',
        answer: 'We advise you to not start developing in advance, since the project you will eventually develop has to be related to the theme of the Hackathon, which is announced at the opening ceremony. However, if you would like to research winning projects from previous years, feel free! You can also start brainstorming with your team well before the start of the Hackathon.',
    },
    {
        question: 'What if I have an urgent question during the Hackathon? Where can I ask?',
        answer: 'We will be setting up a Facebook group for the registered participants. There, you can ask questions during the event. In addition, the Hub members will be around at all times to answer any questions that pop up.',
    },
    {
        question: 'Is there a specific technology or tech stack I need to use for the Hackathon?',
        answer: 'No, there is not. You may use whatever you would like. Keep in mind, however, that the judges tend to reward the projects with more modern tech stacks more than others.',
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
    const answerRef = useRef<HTMLDivElement>(null);
    const [height, setHeight] = useState<number>(0);

    useEffect(() => {
        // Update height when isOpen changes
        if (answerRef.current) {
            const actualHeight = isOpen ? answerRef.current.scrollHeight : 0;
            setHeight(actualHeight);
        }
    }, [isOpen, faq]); // Re-run when FAQ content changes too

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
                    {isOpen && <span className="text-2xl select-none">-</span>}
                    {!isOpen && <span className="text-2xl select-none">+</span>}
                </div>
            </div>
            <div
                style={{
                    height: `${height}px`,
                    overflow: 'hidden',
                    transition: 'height 300ms ease-in-out',
                }}
            >
                <div className="pb-4" ref={answerRef}>
                    <p>{faq.answer}</p>
                </div>
            </div>
        </div>
    );
}

export default function HackathonFAQSection() {
    const [isOpenFaqId, setIsOpenFaqID] = useState(0);

    return (
        <div className={`text-white sm:w-[80%] mx-6 sm:mx-auto py-10 sm:py-20`} id="faq">
            <div className="text-3xl sm:text-4xl flex items-center gap-4 mb-20">
                <img src="./n.png" alt="" className="w-[1.6rem]" />
                <h2>FAQ</h2>
            </div>
            <div>
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
