import { AdminUser } from '@/types/admin';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ROLES } from '@/constants';
import { cn } from '@/lib/utils';

const ROLE_OPTIONS = [
    { value: ROLES.board, label: 'Board' },
    { value: ROLES.dev, label: 'Developer' },
] as const;

export type AdminRole = (typeof ROLE_OPTIONS)[number]['value'];

interface AdminRoleRowProps {
    admin: AdminUser;
    isUpdating: boolean;
    onChangeRole: (newRole: AdminRole) => void;
    className?: string;
}

export const AdminRoleRow = ({ admin, isUpdating, onChangeRole, className }: AdminRoleRowProps) => {
    return (
        <div
            className={cn(
                'flex items-center justify-between gap-4 rounded-xl border border-white/5 bg-white/5 px-4 py-3',
                'hover:bg-white/10 transition-colors',
                isUpdating && 'opacity-70 pointer-events-none',
                className,
            )}
        >
            <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full overflow-hidden bg-white/10 flex items-center justify-center">
                    {admin.avatar_url ? (
                        <img
                            src={admin.avatar_url}
                            alt={admin.name}
                            className="h-full w-full object-cover"
                            onError={(e) => {
                                (e.target as HTMLImageElement).style.visibility = 'hidden';
                            }}
                        />
                    ) : (
                        <span className="text-sm font-semibold text-white/70">
                            {admin.name
                                .split(' ')
                                .map((n) => n[0])
                                .join('')
                                .slice(0, 2)
                                .toUpperCase()}
                        </span>
                    )}
                </div>
                <div className="flex flex-col">
                    <span className="text-sm font-semibold text-white">{admin.name}</span>
                    <span className="text-xs text-white/60">@{admin.username}</span>
                </div>
            </div>

            <div className="w-[180px]">
                <Select
                    value={admin.site_role}
                    onValueChange={(val) => onChangeRole(val as AdminRole)}
                    disabled={isUpdating}
                >
                    <SelectTrigger className="h-9 bg-black/40 border-white/20 text-white">
                        <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                        {ROLE_OPTIONS.map((opt) => (
                            <SelectItem key={opt.value} value={opt.value}>
                                {opt.label}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>
        </div>
    );
};
