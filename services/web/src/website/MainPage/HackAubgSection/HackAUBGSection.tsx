import { Button } from '@/components/ui/button';

export default function HackAUBGSection() {
    return (
        <div className="flex flex-col justify-center">
            <div className="w-[70%] flex mx-auto mb-[20px]">
                <p className="font-mont text-[29px] font-semibold text-blue-950	">HackAUBG</p>
            </div>
            <div className="flex flex-col items-center gap-5 w-[65%] mx-auto">
                <div className="flex justify-between  items-center w-full max-w-[1200px] gap-5">
                    <div className="flex-1 h-[240px] flex flex-col items-center justify-center border border-slate-300 box-border p-2.5 text-center rounded-3xl">
                        <p className=" font-mont text-[90px] font-semibold text-blue-700">52</p>
                        <p className="font-mont text-[19px] text-blue-950">Hours to create a solution</p>
                    </div>
                    <div className="flex-[3] h-[240px] flex flex-row items-end justify-between border rounded-3xl border-slate-300 box-border p-5 bg-[url('/participate.png')] bg-cover bg-center">
                        <div className="flex flex-col w-[55%] ml-[12px]">
                            <p className="font-mont text-[19px] font-semibold text-white ">
                                The biggest student-organized hackathon as of now.
                            </p>
                            <p className="text-blue-200 font-mont text-[12px] mt-[10px]">
                                More than 120 people participated last year.
                            </p>
                        </div>
                        <div>
                            <Button className=" bg-transparent text-white " variant="outline_mono" size="round_sm">
                                Participate
                            </Button>
                        </div>
                    </div>
                </div>
                <div className="flex justify-between items-center w-full max-w-[1200px] gap-5 mb-[20px]">
                    <div className="flex-1 h-[240px] flex flex-col items-start justify-center border  rounded-3xl border-slate-300 box-border p-2.5">
                        <div className=" w-[40%] font-mont font-semibold text-[19px] text-blue-950 mb-[40px] ml-[20px]">
                            <p>Guidance from current industry leaders</p>
                        </div>
                        <div className="flex flex-row  items-center ">
                            <div className="flex flex-row w-[70%] space-x-[-50px] ml-[20px] ">
                                <div className="h-[45%] w-[45%] border border-black rounded-full ">
                                    <img src="../mentor.png" alt="" />
                                </div>
                                <div className="h-[45%] w-[45%] border border-black rounded-full ">
                                    <img src="../mentor.png" alt="" />
                                </div>
                                <div className="h-[45%] w-[45%] border border-black rounded-full ">
                                    <img src="../mentor.png" alt="" />
                                </div>
                            </div>
                            <div className="w-[60%] flex">
                                <Button className="text-blue-700  " variant="outline_mono" size="round_sm">
                                    See all mentors
                                </Button>
                            </div>
                        </div>
                    </div>
                    <div className="flex-1 h-[240px] flex flex-col  border  rounded-3xl border-slate-300 box-border p-2.5 relative text-left">
                        <div className="flex items-start mb-[5px] font-semibold font-mont text-blue-950 mt-[20px] ml-[15px]">
                            <p>Major prize pool</p>
                        </div>

                        <div className="flex justify-center items-center items-baseline">
                            <p className="font-mont text-[90px]  font-bold bg-gradient-to-r from-blue-700  to-teal-400 bg-clip-text text-transparent">
                                6000
                            </p>
                            <div className="font-mont text-[16px] text-blue-950">
                                <p>BGN</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
