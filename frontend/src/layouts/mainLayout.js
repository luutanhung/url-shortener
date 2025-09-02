"use client";

import { Layout } from "antd";

import { Header } from "@/components";

const { Content } = Layout;

export function MainLayout({ children }) {
    return (
        <Layout
            style={{
                minHeight: "100vh",
            }}
        >
            <Header />
            <Content
                className="h-screen"
                style={{
                    paddingTop: "64px",
                }}
            >
                {children}
            </Content>
        </Layout>
    );
}
