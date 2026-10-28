
export const sectionStyles =
    'relative w-full min-h-screen overflow-hidden flex flex-col items-center pb-16 px-4 font-mont bg-[#0f1f38] transition-opacity duration-1000';

export const glowTopStyles =
    'hidden md:block pointer-events-none absolute top-[-265px] left-[289px] z-0 w-[1920px] h-[1920px] opacity-[0.45] blur-[180px] ' +
    'bg-[radial-gradient(circle,#FDC049_0%,transparent_70%)]';

export const glowStyles =
    'hidden md:block pointer-events-none absolute -bottom-60 -right-60 z-0 w-[990px] h-[912px] opacity-[0.45] blur-[180px] ' +
    'bg-[radial-gradient(circle,#FDC049_0%,transparent_70%)]';

export const gearStyles =
    'absolute z-0 pointer-events-none select-none ' +
    'w-[300px] h-[300px] left-[-200px] top-[180px] ' +
    'md:w-[500px] md:h-[500px] md:left-[-320px] md:top-[250px] ' +
    'xl:w-[833px] xl:h-[833px] xl:left-[-450px] xl:top-[210px]';


export const titleStyles =
    "font-['League_Spartan'] font-normal text-4xl sm:text-5xl md:text-7xl lg:text-[96px] leading-none text-center w-full px-4 z-10 " +
    '-mt-4 md:-mt-6 lg:-mt-8 mb-6 md:mb-8';

export const titleWhiteStyles = 'text-white';
export const titleGoldStyles = 'text-[#C79B3B]';

export const subtitleStyles =
    "font-['Rubik'] font-light text-xl md:text-[36px] leading-[1.19] text-[#90D5FF] text-center max-w-[892px] mb-12 md:mb-16 z-10";


export const formFrameStyles =
    'relative z-10 w-full max-w-[1220px] overflow-hidden bg-[#C79B3B] p-3 md:p-[22px]';

export const formCardStyles =
    'relative isolate w-full px-6 py-10 md:pl-16 md:pr-[108px] md:py-16 flex flex-col';

export const formBlurBgStyles =
    'absolute inset-0 -z-10 rounded-[20px] bg-[#163B59] shadow-[4px_4px_20px_2px_#C79B3B] blur-[20px]';

export const fieldGridStyles = 'flex flex-col gap-10 md:gap-14';


export const labelStyles = "font-['Rubik'] font-bold text-lg md:text-[28px] leading-none text-[#90D5FF]";
export const dropdownLabelStyles = labelStyles;


export const inputStyles =
    "!h-[57px] w-full max-w-[1005px] bg-transparent border-2 border-[#90D5FF] rounded-[5px] px-4 " +
    "font-['Rubik'] text-lg md:text-2xl text-[#90D5FF] placeholder:text-[#90D5FF]/80 " +
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#C79B3B]';


export const formControlStyles =
    "!h-[57px] w-full max-w-[1005px] bg-transparent border-2 border-[#90D5FF] rounded-[5px] px-4 " +
    "font-['Rubik'] text-lg md:text-2xl text-[#90D5FF] " +
    'focus:outline-none focus:ring-2 focus:ring-[#C79B3B] ' +
    '[&_svg]:!h-8 [&_svg]:!w-8 [&_svg]:!opacity-100 [&_svg]:text-[#90D5FF] [&_svg]:stroke-[1.5]';


export const dropdownLabelAgeStyles = '!w-[208px] !max-w-[208px]';

export const selectContentStyles =
    'bg-[#163B59] text-[#90D5FF] border-2 border-[#90D5FF] rounded-[5px] max-h-60';

export const radioQuestionStyles =
    "[&>label]:font-['Rubik'] [&>label]:!font-bold [&>label]:!text-lg md:[&>label]:!text-[28px] " +
    '[&>label]:!leading-none [&>label]:!text-[#90D5FF]';



// общото: квадратчетата и отметката
const radioItemStyles =
    '[&[role=radio]]:!h-7 [&[role=radio]]:!w-7 [&[role=radio]]:!rounded-[3px] [&[role=radio]]:!border-2 ' +
    '[&[role=radio]]:!border-[#90D5FF] [&[role=radio]]:!bg-transparent [&[role=radio]]:!relative [&[role=radio]]:!overflow-visible ' +
    '[&[role=radio]_svg]:!hidden ' +
    "[&[role=radio][data-state=checked]]:after:content-['✓'] [&[role=radio][data-state=checked]]:after:absolute " +
    '[&[role=radio][data-state=checked]]:after:left-0 [&[role=radio][data-state=checked]]:after:-bottom-1 ' +
    '[&[role=radio][data-state=checked]]:after:text-[36px] [&[role=radio][data-state=checked]]:after:leading-none ' +
    '[&[role=radio][data-state=checked]]:after:font-bold [&[role=radio][data-state=checked]]:after:text-[#90D5FF]';

// Yes / No – 2 колони (както досега)
export const radioGroupStyles =
    '[&[role=radiogroup]]:!grid [&[role=radiogroup]]:!grid-cols-2 [&[role=radiogroup]]:!mt-6 ' + radioItemStyles;

// 3-те опции за отбор – една под друга на телефон, на един ред на голям екран
export const teamRadioGroupStyles =
    '[&[role=radiogroup]]:!flex [&[role=radiogroup]]:!flex-col [&[role=radiogroup]]:!gap-5 [&[role=radiogroup]]:!mt-6 ' +
    'lg:[&[role=radiogroup]]:!flex-row lg:[&[role=radiogroup]]:!justify-between lg:[&[role=radiogroup]]:!gap-8 ' +
    radioItemStyles;

export const radioOptionLabelStyles =
    "font-['Rubik']  !text-lg md:!text-2xl !leading-none !text-[#90D5FF] ";

export const submitButtonStyles =
    "w-full md:w-[216px] h-[57px] bg-[#C79B3B] hover:bg-[#d6ab4c] text-[#0f1f38] " +
    "font-['Rubik'] font-bold text-2xl rounded-none shadow-[0_4px_4px_rgba(0,0,0,0.4)] transition-colors";

export const errorTextStyles = "font-['Rubik'] text-sm text-red-400 mt-2";
