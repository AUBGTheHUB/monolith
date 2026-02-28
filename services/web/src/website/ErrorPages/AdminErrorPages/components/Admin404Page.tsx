import { AdminErrorTemplatePage } from '../AdminErrorTemplatePage';
import { ERROR_404 } from '../constants';

export function Admin404Page() {
    return <AdminErrorTemplatePage {...ERROR_404} />;
}
