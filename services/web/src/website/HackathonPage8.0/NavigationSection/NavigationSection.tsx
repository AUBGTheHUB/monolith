export const NavigationSection = () => {
    return (
        <div className={`w-full h-[10%] bg-[rgba(26,28,25,1)] border-gray-600 py-2 sticky top-0 z-[100]`}>
            <div className="w-full flex flex-row justify-center items-center">
                <div className="flex flex-row w-[70%] gap-7">
                    <a href="#about">About</a>
                    <a href="#schedule">Schedule</a>
                    <a href="#grading-criteria">Grading Criteria</a>
                    <a href="#faq">FAQ</a>
                </div>
                <div>
                    <a href="/hackathon/registration">Participate now</a>
                </div>
            </div>
        </div>
    );
};
