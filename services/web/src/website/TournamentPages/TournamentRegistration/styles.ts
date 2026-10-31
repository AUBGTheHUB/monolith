export const sectionStyles =
    'relative w-full min-h-screen overflow-hidden flex flex-col items-center pb-16 px-4 font-mont bg-[#04182f] transition-opacity duration-1000';

export const glowStyles =
    'pointer-events-none absolute -bottom-[10%] -right-[35%] z-0 w-[120vw] h-[120vw] max-w-[990px] max-h-[912px] ' +
    'opacity-[0.35] blur-[120px] bg-[radial-gradient(circle,#FDC049_0%,transparent_70%)]';

export const gearStyles =
    'absolute z-0 pointer-events-none select-none h-auto ' +
    'w-[clamp(180px,42vw,520px)] left-[calc(clamp(180px,42vw,520px)*-0.65)] top-[clamp(170px,30vw,360px)]';

export const titleStyles =
    "font-['League_Spartan'] font-normal text-[clamp(1.75rem,6.5vw,4rem)] leading-[0.95] text-center w-full px-4 z-10 " +
    'mb-[clamp(0.75rem,1.5vw,1.5rem)]';

export const titleWhiteStyles = 'text-white';
export const titleGoldStyles = 'text-[#C79B3B]';

export const subtitleStyles =
    "font-['Rubik'] font-light text-[clamp(0.85rem,0.5rem+1.1vw,1.5rem)] leading-[1.19] text-[#90D5FF] text-center w-full px-4 " +
    'mb-[clamp(1.5rem,3vw,2.5rem)] z-10';

export const formFrameStyles =
    'relative z-10 w-[min(92vw,1000px)] overflow-hidden bg-[#C79B3B] p-[clamp(4px,0.2rem+0.8vw,20px)]';

export const formCardStyles =
    'relative isolate w-full flex flex-col rounded-[20px] ' +
    'px-[clamp(1.25rem,0.5rem+3.5vw,4rem)] py-[clamp(1.5rem,0.5rem+3.5vw,4rem)]';

export const formBlurBgStyles =
    'absolute inset-0 -z-10 rounded-[20px] bg-[#163B59] shadow-[4px_4px_20px_2px_#C79B3B] blur-[20px]';

export const fieldGridStyles = 'flex flex-col gap-[clamp(1.25rem,0.8rem+1.5vw,2.25rem)]';

export const labelStyles =
    "font-['Rubik'] font-bold text-[clamp(0.8rem,0.55rem+0.8vw,1.5rem)] leading-tight text-[#90D5FF]";
export const dropdownLabelStyles = labelStyles;

export const inputStyles =
    '!h-[clamp(2.25rem,1.5rem+1.5vw,3.5rem)] w-full min-w-0 bg-transparent border border-[#90D5FF] rounded-[3px] px-3 md:px-4 ' +
    "font-['Rubik'] text-[clamp(0.8rem,0.5rem+0.6vw,1.25rem)] text-[#90D5FF] placeholder:text-[#90D5FF]/80 " +
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#C79B3B]';

export const formControlStyles =
    '!h-[clamp(2.25rem,1.5rem+1.5vw,3.5rem)] !w-full min-w-0 bg-transparent border border-[#90D5FF] rounded-[3px] px-3 md:px-4 ' +
    "font-['Rubik'] text-[clamp(0.8rem,0.5rem+0.6vw,1.25rem)] text-[#90D5FF] " +
    'focus:outline-none focus:ring-2 focus:ring-[#C79B3B] ' +
    '[&_svg]:!h-[clamp(0.9rem,0.6rem+0.6vw,1.5rem)] [&_svg]:!w-[clamp(0.9rem,0.6rem+0.6vw,1.5rem)] ' +
    '[&_svg]:!opacity-100 [&_svg]:text-[#90D5FF] [&_svg]:stroke-[1.5]';

export const ageControlStyles = '!w-[clamp(5.5rem,3rem+8vw,11rem)]';

export const selectContentStyles =
    'bg-[#163B59] text-[#90D5FF] border border-[#90D5FF] rounded-[3px] max-h-60 ' +
    "font-['Rubik'] text-[clamp(0.8rem,0.5rem+0.6vw,1.25rem)]";

export const radioQuestionStyles =
    "[&>label]:font-['Rubik'] [&>label]:!font-bold [&>label]:!text-[clamp(0.8rem,0.55rem+0.8vw,1.5rem)] " +
    '[&>label]:!leading-tight [&>label]:!text-[#90D5FF]';

const radioItemStyles =
    '[&[role=radio]]:!h-[clamp(1rem,0.6rem+0.8vw,1.75rem)] [&[role=radio]]:!w-[clamp(1rem,0.6rem+0.8vw,1.75rem)] [&[role=radio]]:!shrink-0 ' +
    '[&[role=radio]]:!rounded-[3px] [&[role=radio]]:!border-2 [&[role=radio]]:!border-[#90D5FF] ' +
    '[&[role=radio]]:!bg-transparent [&[role=radio]]:!relative [&[role=radio]]:!overflow-visible ' +
    '[&[role=radio]_svg]:!hidden ' +
    "[&[role=radio][data-state=checked]]:after:content-['✓'] [&[role=radio][data-state=checked]]:after:absolute " +
    '[&[role=radio][data-state=checked]]:after:left-0 [&[role=radio][data-state=checked]]:after:-bottom-0.5 ' +
    '[&[role=radio][data-state=checked]]:after:text-[clamp(1.25rem,0.8rem+1vw,2.1rem)] [&[role=radio][data-state=checked]]:after:leading-none ' +
    '[&[role=radio][data-state=checked]]:after:font-bold [&[role=radio][data-state=checked]]:after:text-[#90D5FF]';

export const radioGroupStyles =
    '[&[role=radiogroup]]:!grid [&[role=radiogroup]]:!grid-cols-2 [&[role=radiogroup]]:!gap-4 [&[role=radiogroup]]:!mt-3 ' +
    radioItemStyles;

export const teamRadioGroupStyles =
    '[&[role=radiogroup]]:!flex [&[role=radiogroup]]:!flex-wrap [&[role=radiogroup]]:!gap-x-8 [&[role=radiogroup]]:!gap-y-3 ' +
    '[&[role=radiogroup]]:!mt-3 ' +
    radioItemStyles;

export const radioOptionLabelStyles =
    "font-['Rubik'] font-bold !text-[clamp(0.8rem,0.5rem+0.7vw,1.35rem)] !leading-tight !text-[#90D5FF]";

export const submitButtonStyles =
    'w-[clamp(6rem,3.5rem+5vw,13rem)] h-[clamp(2.25rem,1.4rem+1.5vw,3.25rem)] bg-[#C79B3B] hover:bg-[#d6ab4c] text-[#0f1f38] ' +
    "font-['Rubik'] font-bold text-[clamp(0.85rem,0.5rem+0.8vw,1.5rem)] rounded-none shadow-[0_4px_4px_rgba(0,0,0,0.4)] transition-colors";

export const errorTextStyles = "font-['Rubik'] text-sm text-red-400 mt-2";
