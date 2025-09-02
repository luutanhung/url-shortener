"use client";

import { Button, Layout, Menu, Typography } from "antd";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { logout } from "@/lib";
import { useAuthStore } from "@/stores";

const { Header: AntHeader } = Layout;
const { Title } = Typography;

export const Header = () => {
    const pathname = usePathname();
    const { user, clearCredentials } = useAuthStore();

    const menuItems = [
        {
            key: "/",
            label: <Link href="/">Home</Link>,
        },
    ];

    return (
        <AntHeader
            style={{
                position: "fixed",
                zIndex: 1,
                width: "100%",
                display: "flex",
                alignItems: "center",
                background: "#fff",
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                padding: "0 24px",
                height: "64px",
            }}
        >
            <div
                style={{
                    width: "100%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "flex-start",
                    margin: "0 auto",
                    padding: "0 24px",
                    gap: "16px",
                }}
            >
                <Title level={3}>URL Shortener</Title>
                <Menu
                    mode="horizontal"
                    selectedKeys={[pathname]}
                    items={menuItems}
                    style={{
                        border: "none",
                        background: "transparent",
                        flex: 1,
                        justifyContent: "flex-start",
                        alignItems: "center",
                        borderBottom: "none",
                    }}
                />
            </div>
            <div
                style={{
                    display: "flex",
                    justifyContent: "flex-end",
                    alignItems: "center",
                    gap: "16px",
                }}
            >
                {user ? (
                    <>
                        <Link href="/account">
                            <Button type="primary">Account</Button>
                        </Link>
                        <Button danger onClick={logout} className="ml-2">
                            Logout
                        </Button>
                    </>
                ) : (
                    <>
                        <Link href="/auth/login">
                            <Button type="primary">Login</Button>
                        </Link>
                        <Link href="/auth/register">
                            <Button>Register</Button>
                        </Link>
                    </>
                )}
            </div>
        </AntHeader>
    );
};
