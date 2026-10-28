interface EventCardContent {
    question: string;
    answer: string;
    image: string;
}

export default function FAQCard({ question, answer, image }: EventCardContent) {
    return (
        <div className="flex items-center border border-[#C79B3B] rounded-2xl px-5 py-4 gap-4">
            <img src={`${image}`} className="w-20 h-20 object-contain shrink-0" alt="" />
            <div className="text-[#90D5FF] min-w-0 text-left">
                <h5 className="text-2xl font-league font-bold leading-tight">{question}</h5>
                <div className="text-xl font-normal leading-snug">{answer}</div>
            </div>
        </div>
    );
}
