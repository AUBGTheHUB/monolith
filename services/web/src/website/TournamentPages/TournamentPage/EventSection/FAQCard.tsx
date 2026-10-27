interface EventCardContent {
    question: string;
    answer: string;
    image: string;
}

export default function FAQCard({ question, answer, image }: EventCardContent) {
    return (
        <div className="flex items-center border-2 rounded-2xl p-3 md:p-8 gap-3 border-[#C79B3B]">
            <img src={`${image}`} className="w-[32px] h-auto md:w-[56px] shrink-0" alt="" />
            <div className="text-[#90D5FF] min-w-0">
                <h5 className="text-base md:text-2xl font-bold">{question}</h5>
                <div className="text-sm md:text-xl font-normal">{answer}</div>
            </div>
        </div>
    );
}
