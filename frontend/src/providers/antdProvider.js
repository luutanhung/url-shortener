"use client";

import { AntdRegistry } from "@ant-design/nextjs-registry";
import { App as AntdApp, ConfigProvider, theme } from "antd";

export function AntdProvider({ children }) {
    return (
        <AntdRegistry>
            <ConfigProvider
                theme={{
                    algorithm: theme.defaultAlgorithm,
                    token: {
                        colorPrimary: "#1890ff",
                    },
                }}
            >
                <AntdApp>{children}</AntdApp>
            </ConfigProvider>
        </AntdRegistry>
    );
}
