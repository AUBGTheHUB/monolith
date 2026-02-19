export const MOCK_ADMINS: Record<string, { password: string; name: string }> = {
    'admin@thehub.com': { password: 'admin123', name: 'Admin' },
};

export function validateAdminCredentials(username: string, password: string) {
    const rec = MOCK_ADMINS[username.toLowerCase()];
    if (!rec || rec.password !== password) {
        return { ok: false as const, reason: 'Invalid email or password.' };
    }
    return { ok: true as const, user: { username, name: rec.name } };
}
