import { Control } from 'react-hook-form';
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form.tsx';
import { Input } from '@/components/ui/input.tsx';
import { MultiSelect } from '@/components/ui/multi-select.tsx';
import { TeamMemberFormFieldMessages as MESSAGES } from '../messages.tsx';
import { TeamMemberFormData } from '../validation/validation.tsx';
import { AVAILABLE_DEPARTMENTS } from '../constants.tsx';

interface TeamMemberFormFieldsProps {
    control: Control<TeamMemberFormData>;
}

export function TeamMemberFormFields({ control }: TeamMemberFormFieldsProps) {
    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                    control={control}
                    name="name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>{MESSAGES.LABELS.NAME}</FormLabel>
                            <FormControl>
                                <Input placeholder={MESSAGES.PLACEHOLDERS.NAME} {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={control}
                    name="position"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>{MESSAGES.LABELS.POSITION}</FormLabel>
                            <FormControl>
                                <Input placeholder={MESSAGES.PLACEHOLDERS.POSITION} {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            </div>

            <FormField
                control={control}
                name="avatar_url"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>{MESSAGES.LABELS.IMAGE}</FormLabel>
                        <FormControl>
                            <Input placeholder={MESSAGES.PLACEHOLDERS.IMAGE} {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />

            <FormField
                control={control}
                name="departments"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>{MESSAGES.LABELS.DEPARTMENT}</FormLabel>
                        <FormControl>
                            <MultiSelect
                                options={AVAILABLE_DEPARTMENTS}
                                selected={field.value}
                                onChange={field.onChange}
                                placeholder={MESSAGES.PLACEHOLDERS.DEPARTMENT}
                            />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />

            <div className="space-y-4 pt-4 border-t border-white/10">
                <h3 className="text-lg font-medium text-white">Social Links</h3>

                <FormField
                    control={control}
                    name="social_links.linkedin"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>{MESSAGES.LABELS.SOCIAL_LINKEDIN}</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder={MESSAGES.PLACEHOLDERS.SOCIAL_LINKEDIN}
                                    {...field}
                                    value={field.value || ''}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={control}
                    name="social_links.github"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>{MESSAGES.LABELS.SOCIAL_GITHUB}</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder={MESSAGES.PLACEHOLDERS.SOCIAL_GITHUB}
                                    {...field}
                                    value={field.value || ''}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={control}
                    name="social_links.website"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>{MESSAGES.LABELS.SOCIAL_WEBSITE}</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder={MESSAGES.PLACEHOLDERS.SOCIAL_WEBSITE}
                                    {...field}
                                    value={field.value || ''}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            </div>
        </div>
    );
}
