"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
    Alert,
    Grid,
    Input,
    List,
    notification,
    Select,
    Space,
    Spin,
} from "antd";
import { debounce } from "lodash";
import { useCallback, useState } from "react";

import { URLDetailsCard } from "@/components";
import { MainLayout } from "@/layouts";
import { api } from "@/lib";
import { useAuthStore } from "@/stores";

const { Option } = Select;
const { useBreakpoint } = Grid;

export default function DashboardPage() {
    const { accessToken } = useAuthStore();
    const [notificationApi, contextHolder] = notification.useNotification();
    const queryClient = useQueryClient();
    const [sortDirection, setSortDirection] = useState("desc");
    const [orderBy, setOrderBy] = useState("created_at");
    const [searchTerm, setSearchTerm] = useState("");
    const screens = useBreakpoint();

    const sortFields = [
        { label: "Creation Date", value: "created_at" },
        { label: "Last Accessed", value: "last_accessed" },
        { label: "Click Count", value: "clicks" },
    ];

    const sortDirections = [
        { label: "⬆️", value: "asc" },
        { label: "⬇️", value: "desc" },
    ];

    const { data, isPending, isError } = useQuery({
        queryKey: ["urls", orderBy, sortDirection, searchTerm],
        queryFn: async () => {
            const res = await api.get("/urls", {
                params: {
                    order_by: orderBy,
                    direction: sortDirection,
                    search: searchTerm,
                },
            });
            return res.data;
        },
        enabled: !!accessToken,
    });

    const deleteUrlMutation = useMutation({
        mutationFn: (shortCode) => api.delete(`/urls/${shortCode}`),
        onSuccess: () => {
            notificationApi.success({
                message: "Success",
                description: `URL deleted successfully`,
                placement: "topRight",
            });
            queryClient.invalidateQueries(["urls"]);
        },
        onError: (err) => {
            notificationApi.error({
                message: "Error",
                description:
                    error?.response?.data?.detail || "Failed to delete URL",
            });
        },
    });

    const debouncedSetSearchTerm = useCallback(
        debounce((value) => {
            setSearchTerm(value);
        }, 300),
        []
    );

    const onSearchTermChange = (e) => {
        debouncedSetSearchTerm(e.target.value);
    };

    return (
        <MainLayout>
            {contextHolder}
            <div
                className="max-w-4xl"
                style={{
                    margin: "0 auto",
                    paddingTop: "1rem",
                    paddingLeft: screens.xs
                        ? "1rem"
                        : screens.sm
                          ? "2rem"
                          : "0",
                    paddingRight: screens.xs
                        ? "1rem"
                        : screens.sm
                          ? "2rem"
                          : "0",
                }}
            >
                <div className="flex justify-between items-center mb-4">
                    <Input.Search
                        placeholder="Search URLs..."
                        onChange={onSearchTermChange}
                        style={{
                            width: screens.xs ? "150px" : "200px",
                        }}
                        allowClear
                    />
                    <Space>
                        <Select
                            value={orderBy}
                            onChange={(value) => setOrderBy(value)}
                        >
                            {sortFields.map((field) => (
                                <Option key={field.value} value={field.value}>
                                    {field.label}
                                </Option>
                            ))}
                        </Select>

                        <Select
                            value={sortDirection}
                            onChange={(val) => setSortDirection(val)}
                        >
                            {sortDirections.map((field) => (
                                <Option key={field.value} avlue={field.value}>
                                    {field.label}
                                </Option>
                            ))}
                        </Select>
                    </Space>
                </div>

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

                {data && data.urls.length > 0 && (
                    <List
                        grid={{ gutter: 16, column: 1 }}
                        dataSource={data.urls}
                        renderItem={(url) => (
                            <List.Item key={url.id}>
                                <URLDetailsCard
                                    url={url}
                                    onDeleteUrl={() =>
                                        deleteUrlMutation.mutate(url.short_code)
                                    }
                                />
                            </List.Item>
                        )}
                    />
                )}
            </div>
        </MainLayout>
    );
}
