"use client";

import { QueryClientProvider } from "@tanstack/react-query";

import queryClient from "@/utils/queryClient";

export function QueryProvider({ children }) {
    return (
        <QueryClientProvider client={queryClient}>
            {children}
        </QueryClientProvider>
    );
}
