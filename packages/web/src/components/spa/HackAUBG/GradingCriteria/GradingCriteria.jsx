import { GradingCriteriaDesktop } from './GradingCriteriaDesktop/GradingCriteriaDesktop';
import { GradingCriteriaMobile } from './GradingCriteriaMobile/GradingCriteriaMobile';
import { useMediaQuery } from 'react-responsive';

export const GradingCriteria = () => {
    const isMobile = useMediaQuery({ query: '(max-width: 900px)' });
    console.log(isMobile);
    if (!isMobile) {
        return <GradingCriteriaDesktop />;
    } else {
        return <GradingCriteriaMobile />;
    }
};
