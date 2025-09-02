"use client";

import { MenuOutlined } from "@ant-design/icons";
import { Button, Drawer, Grid, Image, Layout, Menu } from "antd";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

import { logout } from "@/lib";
import { useAuthStore } from "@/stores";

import { UserActions } from "./UserActions";

const { Header: AntHeader } = Layout;
const { useBreakpoint } = Grid;

export const Header = () => {
    const pathname = usePathname();
    const { user } = useAuthStore();
    const screens = useBreakpoint();

    const [drawerVisible, setDrawerVisible] = useState(false);

    const showDrawer = () => {
        setDrawerVisible(true);
    };

    const closeDrawer = () => {
        setDrawerVisible(false);
    };

    const handleMenuItemClick = () => {
        if (!screens.md) {
            closeDrawer();
        }
    };

    const menuItems = [
        {
            key: "/",
            label: <Link href="/">Home</Link>,
        },
        ...(user
            ? [
                  {
                      key: "/dashboard",
                      label: <Link href="/dashboard">Dashboard</Link>,
                  },
              ]
            : []),
    ];

    const isMobile = screens.xs || screens.sm;

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
                padding: screens.md ? "0 5rem" : "0 .5rem",
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
                    padding: isMobile ? "0" : "0 24px",
                    gap: isMobile ? "0" : "16px",
                }}
            >
                <Link href="/" className="flex justify-center items-center">
                    <Image
                        src="/url-shortener-logo.png"
                        alt="URL Shortener Logo"
                        preview={false}
                        style={{ height: "36px" }}
                    />
                </Link>

                {/* Desktop Menu */}
                {screens.md ? (
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
                ) : (
                    // Mobile Menu Toggle
                    <Button
                        type="primary"
                        icon={<MenuOutlined />}
                        style={{ marginLeft: "auto" }}
                        onClick={showDrawer}
                    />
                )}
            </div>

            {screens.md && (
                <div
                    style={{
                        display: "flex",
                        justifyContent: "flex-end",
                        alignItems: "center",
                        gap: "16px",
                    }}
                >
                    <UserActions user={user} logout={logout} />
                </div>
            )}

            {/* Mobile Drawer */}
            {!screens.md && (
                <Drawer
                    title="Menu"
                    placement="right"
                    width={250}
                    onClose={closeDrawer}
                    open={drawerVisible}
                >
                    <Menu
                        mode="vertical"
                        selectedKeys={[pathname]}
                        items={menuItems}
                        style={{ borderRight: "none" }}
                        onClick={handleMenuItemClick}
                    />
                    <UserActions user={user} logout={logout} />
                </Drawer>
            )}
        </AntHeader>
    );
};
