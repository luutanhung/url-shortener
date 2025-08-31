"use client";

import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Button, Card, Form, Input, Typography } from "antd";
import { useRouter } from "next/navigation";
import { useState } from "react";

import api from "@/utils/axios";

const { Title, Text, Link } = Typography;

export default function RegisterPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const res = await api.post("/auth/register", values);
      router.push("/auth/login");
    } catch (err) {
      console.error(err?.response?.data?.message || "Registration failed!");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="flex justify-center items-center min-h-screen">
      <Card>
        <div className="mb-6">
          <Title level={2}>Register</Title>
          <Text>Create an account to get started.</Text>
        </div>
        <Form
          name="register_form"
          layout="vertical"
          autoComplete="off"
          requiredMark="optional"
          onFinish={onFinish}
        >
          <Form.Item
            name="email"
            rules={[
              {
                type: "email",
                required: true,
                message: "Please input your Email!",
              },
            ]}
          >
            <Input prefix={<MailOutlined />} placeholder="Email" />
          </Form.Item>
          <Form.Item
            name="pwd"
            rules={[
              {
                required: true,
                message: "Please input your Password!",
              },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              type="password"
              placeholder="Password"
            />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block loading={loading}>
              Register
            </Button>
            <div className="mt-6 flex justify-between items-center">
              <Text>Already have an account?</Text>{" "}
              <Link href="/auth/login">Login</Link>
            </div>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
