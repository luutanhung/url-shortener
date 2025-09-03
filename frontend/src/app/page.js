"use client";

import { useMutation } from "@tanstack/react-query";
import {
    Button,
    Card,
    DatePicker,
    Form,
    Input,
    notification,
    Typography,
} from "antd";
import dayjs from "dayjs";
import { useState } from "react";

import { BASE_API_URL } from "@/config/environments";
import { MainLayout } from "@/layouts";
import { api } from "@/lib";
import { useAuthStore } from "@/stores";

const { Text } = Typography;

export default function MainPage() {
    const [shortCode, setShortCode] = useState(null);
    const [form] = Form.useForm();
    const [notificationApi, contextHolder] = notification.useNotification();
    const { user } = useAuthStore();

    const validateFutureDate = (_, value) => {
        if (value && value.isBefore(dayjs())) {
            return Promise.reject(
                new Error("Expiration date cannot be in the past!")
            );
        }
        return Promise.resolve();
    };

    const { mutate, isPending, isError, error } = useMutation({
        mutationFn: async (values) => {
            const payload = {
                ...values,
                expires_at: values.expires_at
                    ? values.expires_at.toISOString()
                    : null,
                created_by: user ? user.id : null,
            };

            const res = await api.post("/shorten", payload);
            return res.data;
        },
        onSuccess: (data) => {
            const shortCode = data.short_code;
            if (shortCode !== form.getFieldValue("short_code")) {
                notificationApi.success({
                    message: "Success",
                    description: `This URL has already been shortened. You can use the existing short code: ${shortCode}`,
                });
            } else {
                notificationApi.success({
                    message: "Success",
                    description: `New short code: ${shortCode}`,
                });
            }
            setShortCode(shortCode);
        },
        onError: (err) => {
            console.log(err);
            console.error(
                err?.response?.data?.detail || "URL shortening failed!"
            );
            notificationApi.error({
                message: "Error",
                description:
                    err?.response?.data?.detail || "URL shortening failed!",
            });
        },
    });

    const onFinish = async (values) => {
        mutate(values);
    };

    return (
        <MainLayout>
            {contextHolder}
            <div
                className="flex justify-center items-center px-4"
                style={{
                    paddingTop: "150px",
                }}
            >
                <Card className="w-full max-w-md">
                    <Form
                        form={form}
                        name="shorten_url_form"
                        layout="vertical"
                        onFinish={onFinish}
                        initialValues={{
                            original_url: "",
                            short_code: null,
                        }}
                    >
                        <Form.Item
                            label="Enter URL to shorten"
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
                        <Form.Item name="short_code" label="Custom Short Code">
                            <Input placeholder="Enter your desired custom short code" />
                        </Form.Item>
                        <Form.Item
                            name="expires_at"
                            label="Expires At"
                            rules={[
                                {
                                    validator: validateFutureDate,
                                },
                            ]}
                        >
                            <DatePicker
                                showTime
                                format="YYYY-MM-DD HH:mm:ss"
                                placeholder="Select expiration date"
                            />
                        </Form.Item>
                        <Form.Item>
                            <Button
                                type="primary"
                                htmlType="submit"
                                className="w-full"
                                loading={isPending}
                            >
                                {isPending ? "Shortening... " : "Shorten"}
                            </Button>
                        </Form.Item>

                        {shortCode && (
                            <Form.Item>
                                <Text>
                                    Shortened URL:{" "}
                                    <a
                                        href={`${BASE_API_URL}/${shortCode}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        {shortCode}
                                    </a>
                                </Text>
                            </Form.Item>
                        )}
                    </Form>
                </Card>
            </div>
        </MainLayout>
    );
}
