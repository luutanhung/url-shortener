"use client";

import { useMutation } from "@tanstack/react-query";
import { Button, Card, Form, Input, Layout, Typography } from "antd";
import { useState } from "react";

import { API_URL } from "@/config/environments";
import { MainLayout } from "@/layouts";
import api from "@/utils/axios";

const { Content } = Layout;
const { Text } = Typography;

export default function MainPage() {
    const [shortCode, setShortCode] = useState(null);

    const { mutate, isPending, isError, error } = useMutation({
        mutationFn: (values) => api.post("/api/shorten", values),
        onSuccess: (res) => {
            setShortCode(res.data.data.short_code);
        },
        onError: (err) => {
            console.log(
                err?.response?.data?.message || "URL shortening failed!"
            );
        },
    });

    const onFinish = async (values) => {
        mutate(values);
    };

    return (
        <MainLayout>
            <div className="flex justify-center items-center min-h-screen px-4">
                <Card className="w-full max-w-md">
                    <Form
                        name="shorten_url_form"
                        layout="vertical"
                        onFinish={onFinish}
                    >
                        <Form.Item
                            label="Original URL"
                            name="original_url"
                            rules={[
                                {
                                    required: true,
                                    message: "Please enter the URL!",
                                },
                                {
                                    type: "url",
                                    message: "Please enter a valid URL!",
                                },
                            ]}
                        >
                            <Input placeholder="https://example.com" />
                        </Form.Item>
                        <Form.Item>
                            <Button
                                type="primary"
                                htmlType="submit"
                                className="w-full"
                                loading={isPending}
                            >
                                {isPending ? "Shortening... " : "Shorten URL"}
                            </Button>
                        </Form.Item>

                        {shortCode && (
                            <Form.Item>
                                <Text>
                                    Shortened URL:{" "}
                                    <a
                                        href={`${API_URL}/${shortCode}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        {shortCode}
                                    </a>
                                </Text>
                            </Form.Item>
                        )}
                        {isError && <Text type="danger">{error.message}</Text>}
                    </Form>
                </Card>
            </div>
        </MainLayout>
    );
}
