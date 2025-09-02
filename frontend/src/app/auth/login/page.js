"use client";

import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Button, Card, Checkbox, Form, Input, Typography } from "antd";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import api from "@/utils/axios";

const { Title, Text } = Typography;

export default function LoginPage() {
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const onFinish = async (values) => {
        setLoading(true);
        try {
            const res = await api.post("/auth/jwt/login", values);
            const token = res.data.access_token;
            localStorage.setItem("token", token);
            router.push("/dashboard");
        } catch (error) {
            console.err(response?.data?.message || "Login failed!");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex justify-center items-center min-h-screen">
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
                        <Input prefix={<MailOutlined />} placeholder="Email" />
                    </Form.Item>
                    <Form.Item
                        label="Password"
                        name="pwd"
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
                            loading={loading}
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
    );
}
