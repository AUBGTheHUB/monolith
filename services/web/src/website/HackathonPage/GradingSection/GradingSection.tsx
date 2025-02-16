import { Fragment } from 'react/jsx-runtime';
const POINTS_TD_CLASS_NAME = 'p-4 text-right text-[#009CF9]';
const CRITERIA_TD_CLASS_NAME = 'p-4 text-white w-full';
const TABLE_CLASS_NAME = 'w-full sm:mt-14 border border-separate border-gray-600 rounded-lg  backdrop-blur-md';
const BORDER_ROW_CLASS_NAME = 'w-[95%] mx-auto border-gray-600 border-[0.5px]';
const HEADER_TD_CLASS_NAME = 'text-[#A9B4C2] p-4';

export default function GradingSection() {
    return (
        <div className="relative w-full flex font-mont bg-[#000912] justify-center">
            <div className="relative flex flex-col z-10 my-24 w-full sm:w-4/5">
                <div className="sm:text-4xl text-3xl flex text-left items-center mb-7 ">
                    <img src="./n.png" alt="" className="w-[1.6rem]" />
                    <p className="text-white ml-5 tracking-[0.2em]">GRADING CRITERIA</p>
                </div>

                <div className="flex flex-col justify-center">
                    <div
                        key={projectIdea.category}
                        className="flex flex-col sm:flex-row items-start mb-10 relative justify-center"
                    >
                        <div className="w-full sm:text-lg text-base">
                            <table className={TABLE_CLASS_NAME}>
                                <td className="w-1/2">
                                    <tr className="w-full">
                                        <td className={HEADER_TD_CLASS_NAME}>{projectIdea.category}</td>
                                        <td className={HEADER_TD_CLASS_NAME}>Points</td>
                                    </tr>
                                    <tbody className="w-full">
                                        {projectIdea.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className={CRITERIA_TD_CLASS_NAME}>{criteria}</td>
                                                    <td className={POINTS_TD_CLASS_NAME}>{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className={BORDER_ROW_CLASS_NAME} />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </td>
                                <td className="w-1/2">
                                    <tr className="w-full">
                                        <td className="text-[#A9B4C2] p-4">{projectRealization.category}</td>
                                        <td className="text-[#A9B4C2] p-4 text-right">Points</td>
                                    </tr>
                                    <tbody>
                                        {projectRealization.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className={CRITERIA_TD_CLASS_NAME}>{criteria}</td>
                                                    <td className={POINTS_TD_CLASS_NAME}>{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className={BORDER_ROW_CLASS_NAME} />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </td>
                            </table>
                            <table></table>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col justify-center">
                    <div
                        key={projectComplexity.category}
                        className="flex flex-col sm:flex-row items-start mb-10 relative justify-center"
                    >
                        <div className="w-full sm:text-lg text-base justify-center">
                            <table className={TABLE_CLASS_NAME}>
                                <td className="w-1/2">
                                    <tr className="w-full">
                                        <td className={HEADER_TD_CLASS_NAME}>{projectComplexity.category}</td>
                                        <td className={HEADER_TD_CLASS_NAME}>Points</td>
                                    </tr>
                                    <tbody className="w-full">
                                        {projectComplexity.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className={CRITERIA_TD_CLASS_NAME}>{criteria}</td>
                                                    <td className={POINTS_TD_CLASS_NAME}>{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className={BORDER_ROW_CLASS_NAME} />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </td>
                                <td className="w-1/2">
                                    <tr className="w-full">
                                        <td className={HEADER_TD_CLASS_NAME}>{presentation.category}</td>
                                        <td className={HEADER_TD_CLASS_NAME}>Points</td>
                                    </tr>
                                    <tbody>
                                        {presentation.criteria.map(({ criteria, points }, idx) => (
                                            <Fragment key={idx}>
                                                <tr className="w-full">
                                                    <td className={CRITERIA_TD_CLASS_NAME}>{criteria}</td>
                                                    <td className={POINTS_TD_CLASS_NAME}>{points}</td>
                                                </tr>
                                                {idx !== criteria.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className={BORDER_ROW_CLASS_NAME} />
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
