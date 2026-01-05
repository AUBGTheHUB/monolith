import { Button } from '@/components/ui/button';
import { Field, FieldDescription, FieldError, FieldLabel } from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { zodResolver } from '@hookform/resolvers/zod';
import { ArrowLeft, Trash } from 'lucide-react';
import Dropzone, { FileWithPath } from 'react-dropzone';
import { Controller, useForm } from 'react-hook-form';
import { Link } from 'react-router';
import { z } from 'zod';

const ONE_MEGABYTE = 1 * 1024 * 1024;
const ACCEPT = {
    'image/png': ['.png'],
    'image/jpeg': ['.jpeg'],
    'image/jpg': ['.jpg'],
    'image/webp': ['.webp'],
    'image/gif': ['.gif'],
    'image/svg+xml': ['.svg'],
};

// todo move schemas after api is added
const zImage = z
    .custom<FileWithPath[]>()
    .refine((file) => file?.length === 1, 'You must upload exactly one file.')
    .refine((file) => {
        console.log(file[0]);
        return file[0].size <= ONE_MEGABYTE;
    }, 'File size should not exceed 1MB.')
    .refine(
        (file) => Object.keys(ACCEPT).includes(file[0].type),
        'Only .png, .jpg, .jpeg, .webp, .gif, and .svg formats are accepted.',
    )
    .optional();

const zAddSponsor = z.strictObject({
    name: z.string().min(1, 'Field is required.').max(64, 'Field should not exceed 64 characters.'),
    description: z.string().min(1, 'Field is required.').max(1024, 'Field should not exceed 1024 characters.'),
    image: zImage,
});

type AddSponsor = z.infer<typeof zAddSponsor>;

export function SponsorsAddPage() {
    const form = useForm<AddSponsor>({
        mode: 'all',
        resolver: zodResolver(zAddSponsor),
        defaultValues: {
            name: '',
            description: '',
        },
    });

    function onSubmit(values: AddSponsor) {
        // todo call api to add sponsor

        console.log(values);
    }

    return (
        <div className="min-h-screen flex justify-center items-center flex-col gap-8">
            <Link to="/dashboard/sponsors">
                <Button className="fixed top-8 left-8" variant="secondary">
                    <ArrowLeft />
                    Back to Sponsors
                </Button>
            </Link>
            <div className="text-xl font-bold text-white">Add a new sponsor!</div>
            <form id="add-sponsor" onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-4">
                <Controller
                    control={form.control}
                    name="name"
                    render={({ field, fieldState }) => (
                        <Field data-invalid={fieldState.invalid}>
                            <FieldLabel className="text-white">Sponsor name</FieldLabel>
                            <Input placeholder="A1" {...field} aria-invalid={fieldState.invalid} />
                            <FieldDescription>The full name of the sponsor</FieldDescription>
                            {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                        </Field>
                    )}
                />
                <Controller
                    control={form.control}
                    name="description"
                    render={({ field, fieldState }) => (
                        <Field data-invalid={fieldState.invalid}>
                            <FieldLabel className="text-white">Sponsor description</FieldLabel>
                            <Textarea
                                placeholder="Giving us 1000 packs of energy drinks..."
                                {...field}
                                aria-invalid={fieldState.invalid}
                            />
                            <FieldDescription>Any other relevant information about the sponsor</FieldDescription>
                            {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                        </Field>
                    )}
                />
                <Controller
                    control={form.control}
                    name="image"
                    render={({ field: { onChange, onBlur, value }, fieldState }) => (
                        <Field data-invalid={fieldState.invalid}>
                            <FieldLabel className="text-white">Sponsor Logo</FieldLabel>
                            <Dropzone
                                accept={ACCEPT}
                                multiple={false}
                                maxFiles={1}
                                maxSize={ONE_MEGABYTE}
                                onDrop={onChange}
                            >
                                {({ getRootProps, getInputProps }) => (
                                    <div className="flex flex-col justify-center">
                                        <div {...getRootProps()}>
                                            <Input {...getInputProps()} onBlur={onBlur} />
                                            <div className="flex flex-col gap-2 justify-center items-center bg-gray-900 text-white p-8 border-2 border-gray-600 border-dashed rounded-md">
                                                <div className="font-bold">File drop zone</div>
                                                <div>Drop or click to add a file</div>
                                            </div>
                                        </div>

                                        {value && (
                                            <div className="flex items-center justify-between gap-3 text-white pt-4">
                                                <div className="flex gap-2">
                                                    <span className="font-bold">{value[0].name}</span>
                                                    <span className="text-gray-400 font-mono">
                                                        {(value[0].size / ONE_MEGABYTE).toFixed(2)} MB
                                                    </span>
                                                </div>
                                                <Button
                                                    variant="destructive"
                                                    onClick={() => form.setValue('image', undefined)}
                                                >
                                                    <Trash />
                                                </Button>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </Dropzone>
                            <FieldDescription>File size must not exceed 1MB (thanks, AWS)</FieldDescription>
                            {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                        </Field>
                    )}
                />
            </form>
            <Button className="bg-gray-800 hover:bg-gray-900" type="submit" form="add-sponsor">
                Submit
            </Button>
        </div>
    );
}
