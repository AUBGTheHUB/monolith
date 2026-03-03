import { useAuthStore } from '@/hooks/useAuthStore';
import { useNavigate } from 'react-router';

export function AdminNavigation() {
    const user = useAuthStore((state) => state.user);
    const navigate = useNavigate();
    const logout = () => {
        useAuthStore.getState().clearAuth();
        navigate('/');
    };
    return (
        <div className={`p-3 flex justify-between bg-white`}>
            <p>Hello, {user?.username}!</p>
            <div>
                <button onClick={logout}>Logout</button>
            </div>
        </div>
    );
}
