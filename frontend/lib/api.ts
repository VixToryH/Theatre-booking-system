"use client";

import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});


api.interceptors.request.use((config) => {
    const access = localStorage.getItem("access");
    if (access) {
        config.headers.Authorization = `Bearer ${access}`;
    }
    return config;
});


api.interceptors.response.use(
    (response) => response,

    async (error) => {
        const originalRequest = error.config;

        
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refresh = localStorage.getItem("refresh");
            if (!refresh) {
                console.log("Користувач не залогінений");
                return Promise.reject(error);
            }

            try {
                const res = await axios.post(
                    "http://127.0.0.1:8000/api/token/refresh/",
                    { refresh }
                );

                const newAccess = res.data.access;
                localStorage.setItem("access", newAccess);

                
                originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                return api(originalRequest);

            } catch (refreshError) {
                console.log("Refresh failed → logout");
                localStorage.removeItem("access");
                localStorage.removeItem("refresh");
            }
        }

        return Promise.reject(error);
    }
);

export default api;
