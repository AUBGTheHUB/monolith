import { useAuthStore } from '@/hooks/useAuthStore';
import { Styles } from '../../AdminStyle.ts';

export function AdminNavigation() {
    const user = useAuthStore((state) => state.user);
    return (
        <div className={`p-3 flex justify-between bg-[${Styles.colors.hubCyan}]`}>
            <p>Hello, {user?.username}!</p>
            <div>
                <button>Logout</button>
            </div>
        </div>
    );
}
