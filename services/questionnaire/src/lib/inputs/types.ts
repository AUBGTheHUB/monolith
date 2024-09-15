export enum InputType {
    TextArea = 'textarea',
    Text = 'text',
    Email = 'email',
}

export type Question = {
    title: string;
    type: InputType;
    body: string;
};
