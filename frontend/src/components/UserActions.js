import { Button, Grid } from "antd";
import Link from "next/link";

const { useBreakpoint } = Grid;

export const UserActions = ({ user, logout }) => {
    const screens = useBreakpoint();

    const isMobile = screens.xs;

    return (
        <>
            {user ? (
                <div
                    style={{
                        display: "flex",
                        flexDirection: isMobile ? "column" : "row",
                        gap: !isMobile ? "1rem" : ".5rem",
                        alignItems: "center",
                    }}
                >
                    <Link href="/account">
                        <Button type="primary" style={{ width: "100%" }}>
                            Account
                        </Button>
                    </Link>
                    <Button color="default" variant="solid" onClick={logout}>
                        Logout
                    </Button>
                </div>
            ) : (
                <div
                    style={{
                        display: "flex",
                        flexDirection: isMobile ? "column" : "row",
                        gap: !isMobile ? "1rem" : ".5rem",
                        alignItems: "center",
                    }}
                >
                    <Link href="/auth/login">
                        <Button type="primary">Login</Button>
                    </Link>
                    <Link href="/auth/register">
                        <Button>Register</Button>
                    </Link>
                </div>
            )}
        </>
    );
};
