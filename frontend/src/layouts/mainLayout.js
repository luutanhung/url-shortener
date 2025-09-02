import { Layout } from "antd";

import { Footer, Header } from "@/components";

const { Content } = Layout;

export function MainLayout({ children }) {
    return (
        <Layout className="min-h-screen">
            <Header />
            <Content>{children}</Content>
            <Footer />
        </Layout>
    );
}
