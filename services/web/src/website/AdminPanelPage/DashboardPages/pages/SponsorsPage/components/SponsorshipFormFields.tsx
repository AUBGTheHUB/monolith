import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { SponsorFormData } from '@/website/AdminPanelPage/DashboardPages/pages/SponsorsPage/validation/sponsor.tsx';
import { SponsorsFormFieldMessages as MESSAGES } from '../messages.tsx';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form.tsx';

const TIERS = ['Platinum', 'Gold', 'Silver', 'Bronze'];

type SponsorFormFieldsProps = {
    control: Control<SponsorFormData>;
};

export function SponsorFormFields({ control }: SponsorFormFieldsProps) {
    return (
        <>
            <InputComponent
                control={control}
                name="name"
                label={MESSAGES.LABELS.NAME}
                placeholder={MESSAGES.PLACEHOLDERS.NAME}
                type="text"
            />

            <FormField
                control={control}
                name="tier"
                render={({ field }) => (
                    <FormItem className="space-y-3">
                        <FormLabel className="text-white font-medium text-sm">{MESSAGES.LABELS.TIER}</FormLabel>
                        <FormControl>
                            <select
                                {...field}
                                className="flex h-10 w-full rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all"
                            >
                                <option value="" disabled className="bg-slate-900 text-gray-500">
                                    {MESSAGES.PLACEHOLDERS.TIER}
                                </option>
                                {TIERS.map((tier) => (
                                    <option key={tier} value={tier} className="bg-slate-900 text-white">
                                        {tier}
                                    </option>
                                ))}
                            </select>
                        </FormControl>
                        <div className="min-h-[24px] !mb-3">
                            <FormMessage />
                        </div>
                    </FormItem>
                )}
            />
            <InputComponent
                control={control}
                name="logo_url"
                label={MESSAGES.LABELS.LOGO}
                placeholder={MESSAGES.PLACEHOLDERS.LOGO}
                type="url"
            />
            <InputComponent
                control={control}
                name="website_url"
                label={MESSAGES.LABELS.WEBSITE}
                placeholder={MESSAGES.PLACEHOLDERS.WEBSITE}
                type="url"
            />
            {/*TODO Add in BE*/}
            {/*<InputComponent*/}
            {/*    control={control}*/}
            {/*    name="careersUrl"*/}
            {/*    label={MESSAGES.LABELS.CAREERS}*/}
            {/*    placeholder={MESSAGES.PLACEHOLDERS.CAREERS}*/}
            {/*    type="url"*/}
            {/*/>*/}
        </>
    );
}
