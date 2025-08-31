"use client";

import { useEffect } from "react";

import api from "@/utils/axios";

export default function HomePage() {
  useEffect(() => {
    api.get("/ping").then((res) => console.log(res));
  });
}
