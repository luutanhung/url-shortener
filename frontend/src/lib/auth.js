import Cookies from "js-cookie";

import { useAuthStore } from "@/stores";

import { api } from "./axios";

export const login = async (credentials) => {
    const formData = new URLSearchParams();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    const res = await api.post("/auth/jwt/login", formData, {
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    const data = res.data.data;
    useAuthStore.getState().setCredentials(data);
    Cookies.set("auth-token", data.access_token, { expires: 7 });

    return data;
};

export const logout = () => {
    useAuthStore.getState().clearCredentials();
    Cookies.remove("auth-token");
    window.location.href = "/";
};
