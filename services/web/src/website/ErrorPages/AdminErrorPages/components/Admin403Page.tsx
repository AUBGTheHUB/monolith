import { AdminErrorTemplatePage } from '../AdminErrorTemplatePage';
import { ERROR_403 } from '../constants';

export function Admin403Page() {
    return <AdminErrorTemplatePage {...ERROR_403} />;
}
