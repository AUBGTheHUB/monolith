import { Button } from '@/components/ui/button';

export default function HackAUBGSection() {
    return (
        <div className="flex flex-col justify-center">
            <div className="w-[90%] flex mx-auto">
                <p>HackAUBG</p>
            </div>
            <div className="flex flex-col items-center gap-5 w-[90%] mx-auto">
                <div className="flex justify-between  items-center w-full max-w-[1200px] gap-5">
                    <div className="flex-1 h-[200px] flex flex-col items-center justify-center border border-black box-border p-2.5 text-center rounded-sm">
                        <p>52</p>
                        <p>Hours to create a solution</p>
                    </div>
                    <div className="flex-[3] h-[200px] flex flex-row items-end justify-between border border-black box-border p-5">
                        <div className="flex flex-col">
                            <p>The biggest student-organized hackathon as of now.</p>
                            <p>More than 120 people participated last year.</p>
                        </div>
                        <div>
                            <Button variant="outline_mono" size="round_sm">
                                Participate
                            </Button>
                        </div>
                    </div>
                </div>
                <div className="flex justify-between items-center w-full max-w-[1200px] gap-5">
                    <div className="flex-1 h-[150px] flex flex-col items-start justify-center border border-black box-border p-2.5">
                        <div>
                            <p>Guidance from current industry leaders</p>
                        </div>
                        <div>
                            <div>
                                <img src="" alt="" />
                                <img src="" alt="" />
                                <img src="" alt="" />
                            </div>
                            <Button variant="outline_mono" size="round_sm">
                                See all mentors
                            </Button>
                        </div>
                    </div>
                    <div className="flex-1 h-[150px] flex flex-col justify-center items-center border border-black box-border p-2.5 relative text-left">
                        <p>Major prize pool</p>
                        <p>6000BGN</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
