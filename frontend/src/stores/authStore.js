import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useAuthStore = create(
    persist(
        (set) => ({
            accessToken: null,
            tokenType: null,
            user: null,
            setCredentials: (data) =>
                set({
                    accessToken: data.access_token,
                    tokenType: data.token_type,
                    user: {
                        id: data.id,
                        email: data.email,
                        username: data.username,
                        is_active: data.is_active,
                    },
                }),
            clearCredentials: () =>
                set({
                    accessToken: null,
                    tokenType: null,
                    user: null,
                }),
        }),
        {
            name: "url-shortener-auth-storage",
            getStorage: () => localStorage,
        }
    )
);
