import { Button } from '@/components/ui/button';

export default function HackAUBGSection() {
    return (
        <div className="flex flex-col justify-center">
            <div className="sm:w-3/5 w-11/12 flex mx-auto mb-[1.25rem]">
                <p className="font-mont text-[1.813rem] font-semibold text-blue-950	">HackAUBG</p>
            </div>
            <div className="flex flex-col items-center gap-5 sm:w-3/5 w-11/12 mx-auto">
                <div className="flex flex-wrap lg:flex-nowrap justify-between  items-center w-full max-w-[75rem] gap-5 ">
                    <div className=" w-full lg:flex-1 h-[15rem] flex flex-col items-center justify-center border border-slate-300 box-border p-5 text-center rounded-3xl">
                        <p className=" font-mont text-[5.625rem] font-semibold text-blue-700">52</p>
                        <p className="font-mont text-[1.188rem] text-blue-950">Hours to create a solution</p>
                    </div>
                    <div className="w-full lg:flex-[3] h-[15rem] flex flex-col items-baseline justify-end  border rounded-3xl border-slate-300 box-border p-5 bg-[url('/participate.png')] bg-cover bg-center">
                        <div className="flex flex-col  lg:w-[70%] sm:w-[100%]">
                            <p className="font-mont text-[1.188rem] font-semibold text-white ">
                                The biggest student-organized hackathon as of now.
                            </p>
                        </div>
                        <div className="flex flex row w-[100%] justify-between">
                            <div>
                                <p className="text-blue-200 font-mont text-[0.75rem] mt-[0.625rem]">
                                    More than 120 people participated last year.
                                </p>
                            </div>
                            <div className="flex items-end">
                                <Button
                                    className="bg-transparent text-white border-white hover:bg-white hover:text-blue-700 transition duration-200"
                                    variant="outline_mono"
                                    size="round_sm"
                                >
                                    Participate
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
                <div className=" flex flex-wrap lg:flex-nowrap justify-between items-center w-full max-w-[75rem] gap-5 mb-[1.25rem]">
                    <div className="w-full lg:flex-1 h-[15rem]  p-5 flex flex-col items-start justify-center border  rounded-3xl border-slate-300 box-border ">
                        <div className=" w-[80%] font-mont font-semibold text-[1.188rem] text-blue-950 mb-[2.5rem]">
                            <p>Guidance from current industry leaders</p>
                        </div>
                        <div className="flex flex-row  items-center ">
                            <div className="flex flex-row w-[70%] lg:space-x-[-3.125rem] space-x-[-25px] ">
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
                            <div className="w-[60%] h-full flex items-end justify-center">
                                <Button
                                    className="text-blue-700 border-blue-700 bg-transparent hover:bg-blue-700 hover:text-white transition duration-200"
                                    variant="outline_mono"
                                    size="round_sm"
                                >
                                    See all mentors
                                </Button>
                            </div>
                        </div>
                    </div>
                    <div className="w-full lg:flex-1 h-[15rem] flex flex-col  border  rounded-3xl border-slate-300 box-border p-5 relative text-left">
                        <div className="flex items-start mb-[0.313rem] font-semibold font-mont text-blue-950 mt-[1.25rem] ">
                            <p>Major prize pool</p>
                        </div>

                        <div className="flex justify-center  items-baseline">
                            <p className="font-mont lg:text-[5.625rem] text-[5.2rem] font-bold bg-gradient-to-r from-blue-700  to-teal-400 bg-clip-text text-transparent">
                                6000
                            </p>
                            <div className="font-mont text-[1rem] text-blue-950">
                                <p>BGN</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
