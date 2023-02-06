import { GradingCriteriaDesktop } from './GradingCriteriaDesktop/GradingCriteriaDesktop';
import { GradingCriteriaMobile } from './GradingCriteriaMobile/GradingCriteriaMobile';
import { useMediaQuery } from 'react-responsive';

export const GradingCriteria = () => {
    const isMobile = useMediaQuery({ query: '(max-width: 1000px)' });

    if (!isMobile) {
        return <GradingCriteriaDesktop />;
    } else {
        return <GradingCriteriaMobile />;
    }
};
