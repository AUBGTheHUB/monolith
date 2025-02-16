import React, { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/dist/ScrollTrigger";

function ScrollSection() {
  const sectionRef = useRef(null);
  const triggerRef = useRef(null);

  gsap.registerPlugin(ScrollTrigger);

  useEffect(() => {
    const pin = gsap.fromTo(
      sectionRef.current,
      {
        translateX: 0,
      },
      {
        translateX: window.innerWidth <= 768 ? "-180vh" : "-420vh", // Adjust based on screen width
        ease: "none",
        duration: 1,
        scrollTrigger: {
          trigger: triggerRef.current,
          start: "top top",
          end: "2000 top",
          scrub: 0.6,
          pin: true,
        },
      }
    );

    return () => {
      // Cleanup the animation on component unmount
      pin.kill();
    };
  }, []);

  return (
    <div>
      <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 ml-[9%] absolute top-0 left-0 flex items-center space-x-4 p-4">
        <img src="./n.png" alt="" className="w-[1.6rem]" />
        <p className="text-white tracking-[0.2em]">JOURNEY</p>
      </div>

      <section className="scroll-section-outer mr-20">
        <div ref={triggerRef} className="mr-20">
          <div ref={sectionRef} className="scroll-section-inner mr-20">
            <div className="scroll-section mr-16 text-white">
              <div className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] w-[100vh] relative">
                <div className="absolute left-[0.30rem] top-[20%] w-1 h-24 bg-white rounded-lg -translate-x-2"></div>
                <h3 className="text-white text-xl mb-2">Present and Win</h3>
                <p className="text-[#A9B4C3] text-md">
                  This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!
                </p>
                <div className="absolute right-6 bottom-0 flex gap-2 translate-y-1/2">
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                </div>
              </div>
            </div>

                        <div className="scroll-section mr-16 text-white">
              <div className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] w-[100vh] relative">
                <div className="absolute left-[0.30rem] top-[20%] w-1 h-24 bg-white rounded-lg -translate-x-2"></div>
                <h3 className="text-white text-xl mb-2">Present and Win</h3>
                <p className="text-[#A9B4C3] text-md">
                  This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!
                </p>
                <div className="absolute right-6 bottom-0 flex gap-2 translate-y-1/2">
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                </div>
              </div>
            </div>

                        <div className="scroll-section mr-16 text-white">
              <div className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] w-[100vh] relative">
                <div className="absolute left-[0.30rem] top-[20%] w-1 h-24 bg-white rounded-lg -translate-x-2"></div>
                <h3 className="text-white text-xl mb-2">Present and Win</h3>
                <p className="text-[#A9B4C3] text-md">
                  This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!
                </p>
                <div className="absolute right-6 bottom-0 flex gap-2 translate-y-1/2">
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                </div>
              </div>
            </div>

                        <div className="scroll-section mr-16 text-white">
              <div className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] w-[100vh] relative">
                <div className="absolute left-[0.30rem] top-[20%] w-1 h-24 bg-white rounded-lg -translate-x-2"></div>
                <h3 className="text-white text-xl mb-2">Present and Win</h3>
                <p className="text-[#A9B4C3] text-md">
                  This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!
                </p>
                <div className="absolute right-6 bottom-0 flex gap-2 translate-y-1/2">
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                </div>
              </div>
            </div>

                        <div className="scroll-section mr-16 text-white">
              <div className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] w-[100vh] relative">
                <div className="absolute left-[0.30rem] top-[20%] w-1 h-24 bg-white rounded-lg -translate-x-2"></div>
                <h3 className="text-white text-xl mb-2">Present and Win</h3>
                <p className="text-[#A9B4C3] text-md">
                  This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!
                </p>
                <div className="absolute right-6 bottom-0 flex gap-2 translate-y-1/2">
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                </div>
              </div>
            </div>

                        <div className="scroll-section mr-16 text-white">
              <div className="border-2 border-[#233340] rounded-md p-6 bg-[#000912] w-[100vh] relative">
                <div className="absolute left-[0.30rem] top-[20%] w-1 h-24 bg-white rounded-lg -translate-x-2"></div>
                <h3 className="text-white text-xl mb-2">Present and Win</h3>
                <p className="text-[#A9B4C3] text-md">
                  This is the home stretch! You have put in the work and now need to blow the judges away! Your task consists of creating a presentation for your product, as well as a Software Demo. After your presentation, there will be a Q&A session with the panel of judges. The grading criteria for the project and presentation can be found below. Make sure to check it, as it is extremely important! If you have any more questions, check out the FAQ section at the end of the page!
                </p>
                <div className="absolute right-6 bottom-0 flex gap-2 translate-y-1/2">
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                  <div className="w-2 h-2 rounded-full bg-white"></div>
                </div>
              </div>
            </div>

            {/* Repeat similar blocks for other content sections... */}
          </div>
        </div>
      </section>
    </div>
  );
}

export default ScrollSection;
