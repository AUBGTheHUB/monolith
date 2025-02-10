import { Fragment } from 'react/jsx-runtime';

export default function GradingSection() {
    return (
        <div className="relative w-full flex justify-center items-center font-mont bg-[#000912]">
            <div className="relative w-full flex flex-col z-10 my-24">
                <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center ">
                    <img src="./n.png" alt="" className="w-[1.6rem]" />
                    <p className="text-white ml-5 tracking-[0.2em]">GRADING CRITERIA</p>
                </div>

                <div className="flex flex-col">
                    <div key={projectIdea.category} className="flex flex-col sm:flex-row items-start mb-10 relative">
                        <div className="w-full sm:w-3/5 sm:text-lg text-base">
                            <table className="w-full sm:mt-14 border border-separate border-gray-600 rounded-lg bg-[#13181C]/80 backdrop-blur-md">
                                <td className="w-1/2">
                                    <tr className="w-full">
                                        <td className="text-[#A9B4C2] p-4">{projectIdea.category}</td>
                                        <td className="text-[#A9B4C2] p-4">Points</td>
                                    </tr>
                                    <tbody className="w-full">
                                        {projectIdea.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className="p-4 text-white">{criteria}</td>
                                                    <td className="p-4 text-right text-[#009CF9]">{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className="w-[95%] mx-auto border-gray-600 border-[0.5px]" />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </td>
                                <td className="w-half">
                                    <tr className="w-full">
                                        <td className="text-[#A9B4C2] p-4">{projectRealization.category}</td>
                                        <td className="text-[#A9B4C2] p-4 text-right">Points</td>
                                    </tr>
                                    <tbody>
                                        {projectRealization.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className="p-4 text-white">{criteria}</td>
                                                    <td className="text-right p-4 text-[#009CF9]">{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className="w-[95%] mx-auto border-gray-600 border-[0.5px]" />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </td>
                            </table>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col">
                    <div
                        key={projectComplexity.category}
                        className="flex flex-col sm:flex-row items-start mb-10 relative"
                    >
                        <div className="w-full sm:w-3/5 sm:text-lg text-base">
                            <table className="w-full sm:mt-14 border border-separate border-gray-600 rounded-lg bg-[#13181C]/80 backdrop-blur-md">
                                <td className="w-1/2">
                                    <tr className="w-full">
                                        <td className="text-[#A9B4C2] p-4">{projectIdea.category}</td>
                                        <td className="text-[#A9B4C2] p-4">Points</td>
                                    </tr>
                                    <tbody className="w-full">
                                        {projectComplexity.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className="p-4 text-white">{criteria}</td>
                                                    <td className="p-4 text-[#009CF9] text-right">{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className="w-[95%] mx-auto border-gray-600 border-[0.5px]" />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </td>
                                <td className="w-1/2">
                                    <tr className="w-full">
                                        <td className="text-[#A9B4C2] p-4">{presentation.category}</td>
                                        <td className="text-[#A9B4C2] p-4">Points</td>
                                    </tr>
                                    <tbody>
                                        {presentation.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className="p-4 text-white">{criteria}</td>
                                                    <td className="p-4 text-[#009CF9] text-right">{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className="w-[95%] mx-auto border-gray-600 border-[0.5px]" />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </td>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
const projectIdea = {
    category: 'PROJECT IDEA',
    criteria: [
        { criteria: 'Innovative idea and originality', points: '8' },
        { criteria: 'Market research', points: '5' },
        { criteria: 'Usage of external data to verify the idea', points: '2' },
    ],
};

const projectRealization = {
    category: 'PROJECT REALIZATION',
    criteria: [
        { criteria: 'UX/UI design', points: '8' },
        { criteria: 'Scalability', points: '5' },
        { criteria: 'Structured git repository with documentation', points: '2' },
        { criteria: 'Project deployment', points: '2' },
    ],
};

const projectComplexity = {
    category: 'COMPLEXITY OF THE PROJECT',
    criteria: [
        { criteria: 'Code originality', points: '8' },
        { criteria: 'Suitable technology stack', points: '5' },
        { criteria: 'Clear coding style', points: '2' },
        { criteria: 'Security', points: '2' },
    ],
};

const presentation = {
    category: 'PRESENTATION',
    criteria: [
        { criteria: 'Coherency', points: '8' },
        { criteria: 'Clear explanation and defense of project ideas', points: '2' },
        { criteria: 'Demo', points: '2' },
        { criteria: 'Demonstration and explanation of the most complex feature of the project', points: '2' },
    ],
};
