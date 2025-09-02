"use client";

import { useQuery } from "@tanstack/react-query";
import { Alert, Card, List, Spin, Typography } from "antd";

import { MainLayout } from "@/layouts";
import { api } from "@/lib";
import { useAuthStore } from "@/stores";

const { Text, Link: AntLink } = Typography;

export default function DashboardPage() {
    const { accessToken } = useAuthStore();

    const { data, isPending, isError } = useQuery({
        queryKey: ["urls"],
        queryFn: async () => {
            const res = await api.get("/urls");
            return res.data.data;
        },
        enabled: !!accessToken,
    });

    return (
        <MainLayout>
            <div
                className="max-w-7xl px-[150px]"
                style={{
                    margin: "0 auto",
                    paddingTop: "1rem",
                }}
            >
                {isPending && (
                    <div className="flex justify-center">
                        <Spin size="large" />
                    </div>
                )}

                {isError && (
                    <Alert
                        message="Error fetching URLs"
                        type="error"
                        showIcon
                    />
                )}

                {data && (
                    <List
                        grid={{ gutter: 16, column: 1 }}
                        dataSource={data}
                        renderItem={(url) => (
                            <List.Item key={url.id}>
                                <Card title={`Short Code: ${url.short_code}`}>
                                    <p>
                                        <Text strong>Original URL:</Text>{" "}
                                        <AntLink
                                            href={url.original_url}
                                            target="_blank"
                                        >
                                            {url.original_url}
                                        </AntLink>
                                    </p>
                                    <p>
                                        <Text strong>Created At:</Text>{" "}
                                        {new Date(
                                            url.created_at
                                        ).toLocaleString()}
                                    </p>
                                    <p>
                                        <Text strong>Clicks:</Text> {url.clicks}
                                    </p>
                                    <p>
                                        <Text strong>Last Accessed:</Text>{" "}
                                        {url.last_accessed
                                            ? new Date(
                                                  url.last_accessed
                                              ).toLocaleString()
                                            : "-"}
                                    </p>
                                    <p>
                                        <Text strong>Expires At:</Text>{" "}
                                        {url.expires_at
                                            ? new Date(
                                                  url.expires_at
                                              ).toLocaleString()
                                            : "-"}
                                    </p>
                                </Card>
                            </List.Item>
                        )}
                    />
                )}
            </div>
        </MainLayout>
    );
}
