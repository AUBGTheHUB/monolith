import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { SponsorFormData } from '@/website/AdminPanelPage/DashboardPages/pages/SponsorsPage/validation/sponsor.tsx';
import { SponsorsFormFieldMessages as MESSAGES } from '../messages.tsx';
import { DropdownComponent } from '@/internalLibrary/DropdownComponent/DropdownComponent.tsx';
const TIERS = ['Platinum', 'Gold', 'Silver', 'Bronze', 'Custom'];

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
            <DropdownComponent
                control={control}
                name="tier"
                label={MESSAGES.LABELS.TIER}
                placeholder={MESSAGES.PLACEHOLDERS.TIER}
                items={TIERS.map((tier) => ({ label: tier, value: tier.toUpperCase(), name: tier }))}
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
