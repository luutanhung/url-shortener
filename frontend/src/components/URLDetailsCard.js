"use client";

import { Button, Card, notification, Space, Typography } from "antd";
import dayjs from "dayjs";

import { BASE_API_URL } from "@/config/environments";

const { Text, Link } = Typography;

export function URLDetailsCard({ url, onDeleteUrl }) {
    if (!url) return null;

    const [notificationApi, contextHolder] = notification.useNotification();

    const copyShortenedUrlHandler = () => {
        navigator.clipboard.writeText(`${BASE_API_URL}/${url.short_code}`);
        notificationApi.success({
            message: "Success",
            description: "The shortened URL has been copied to your clipboard!",
            placement: "topRight",
        });
    };

    return (
        <Card size="small">
            {contextHolder}
            <div className="flex justify-between items-start">
                <div>
                    <p>
                        <Text>Short Code:</Text>{" "}
                        <Link
                            href={`${BASE_API_URL}/${url.short_code}`}
                            target="_blank"
                        >
                            {url.short_code}
                        </Link>
                    </p>
                    <p>
                        <Text>Original URL:</Text>{" "}
                        <Link href={url.original_url} target="_blank">
                            {url.original_url}
                        </Link>
                    </p>
                    <div className="flex justify-start flex-col">
                        {url.last_accessed && (
                            <Text>
                                Last access:{" "}
                                {url.last_accessed
                                    ? dayjs(url.last_accessed).format(
                                          "YYYY-MM-DD HH:mm:ss"
                                      )
                                    : ""}
                            </Text>
                        )}
                        <Text>Clicks: {url.clicks || 0}</Text>
                    </div>
                </div>

                <Space>
                    <Button
                        color="cyan"
                        variant="solid"
                        onClick={copyShortenedUrlHandler}
                    >
                        Copy
                    </Button>
                    <Button
                        color="default"
                        variant="solid"
                        onClick={onDeleteUrl}
                    >
                        Delete
                    </Button>
                </Space>
            </div>
        </Card>
    );
}
