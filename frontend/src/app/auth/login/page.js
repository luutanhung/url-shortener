"use client";

import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { useMutation } from "@tanstack/react-query";
import { Button, Card, Checkbox, Form, Input, Typography } from "antd";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { MainLayout } from "@/layouts";
import { login } from "@/lib";
import { useAuthStore } from "@/stores";

const { Title, Text } = Typography;

export default function LoginPage() {
    const router = useRouter();
    const setCredentials = useAuthStore((state) => state.setCredentials);

    const {
        mutate: loginMutate,
        isPending,
        isError,
        error,
    } = useMutation({
        mutationFn: async (values) => {
            const data = await login(values);
            console.log(data);
        },
        onSuccess: (res) => {
            router.push("/dashboard");
            console.log("login successfully");
        },
        onError: (err) => {
            console.err(response?.data?.message || "Login failed!");
        },
    });

    const onFinish = async (values) => {
        loginMutate(values);
    };

    return (
        <MainLayout>
            <div className="h-full flex justify-center items-center">
                <Card className="max-w-full shadow-lg">
                    <Title level={2} className="text-center mb-6">
                        Login
                    </Title>
                    <Form
                        name="login_form"
                        layout="vertical"
                        autoComplete="off"
                        onFinish={onFinish}
                    >
                        <Form.Item
                            label="Email"
                            name="email"
                            rules={[
                                {
                                    type: "email",
                                    required: true,
                                    message: "Please enter your email!",
                                },
                            ]}
                        >
                            <Input
                                prefix={<MailOutlined />}
                                placeholder="Email"
                            />
                        </Form.Item>
                        <Form.Item
                            label="Password"
                            name="password"
                            rules={[
                                {
                                    required: true,
                                    message: "Please enter your password!",
                                },
                            ]}
                        >
                            <Input.Password
                                prefix={<LockOutlined />}
                                type="password"
                                placeholder="Enter your password"
                            />
                        </Form.Item>
                        <Form.Item className="flex justify-between items-center">
                            <Form.Item
                                name="remember"
                                valuePropName="checked"
                                noStyle
                            >
                                <Checkbox>Remember me</Checkbox>
                            </Form.Item>
                            <Link href="/auth/forgot-password">
                                Forgot password
                            </Link>
                        </Form.Item>
                        <Form.Item>
                            <Button
                                type="primary"
                                htmlType="submit"
                                className="w-full"
                                loading={isPending}
                            >
                                Login
                            </Button>
                            <div className="p-2">
                                <Text>{"Don't have an account?"}</Text>{" "}
                                <Link href="/auth/register">Register now</Link>
                            </div>
                        </Form.Item>
                    </Form>
                </Card>
            </div>
        </MainLayout>
    );
}
