import { Button } from "./Button";

export default {
    title: "Components/Button",
    component: Button,
    argTypes: {
        type: {
            control: "select",
            options: ["primary", "default", "dashed", "link", "text"],
        },
        size: { control: "select", options: ["small", "middle", "large"] },
        onClick: { action: "clicked" },
    },
};

export const Primary = (args) => <Button {...args}>Primary Button</Button>;
Primary.args = {
    type: "primary",
};

export const Default = (args) => <Button {...args}>Default Button</Button>;
Default.args = {
    type: "default",
};

export const Large = (args) => <Button {...args}>Large Button</Button>;
Large.args = {
    type: "large",
};
