export enum InputType {
    TextArea = 'textarea',
    Text = 'text',
}

export type Question = {
    title: string;
    type: InputType;
    body: string;
};
