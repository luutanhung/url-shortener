"use client";

import { Button, Card, Form, Input, Typography } from "antd";
import { useState } from "react";

import { API_URL } from "@/config/environments";
import api from "@/utils/axios";

const { Text } = Typography;

export default function HomePage() {
  const [loading, setLoading] = useState(false);
  const [shortCode, setShortCode] = useState(null);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const res = await api.post("/api/shorten", values);
      setShortCode(res.data.short_code);
    } catch (err) {
      console.error(err?.response?.data?.message || "URL shortening failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen px-4">
      <Card className="w-full max-w-md">
        <Form name="shorten_url_form" layout="vertical" onFinish={onFinish}>
          <Form.Item
            label="Original URL"
            name="original_url"
            rules={[
              { required: true, message: "Please enter the URL!" },
              { type: "url", message: "Please enter a valid URL!" },
            ]}
          >
            <Input placeholder="https://example.com" />
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="w-full"
              loading={loading}
            >
              Shorten URL
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
        </Form>
      </Card>
    </div>
  );
}
