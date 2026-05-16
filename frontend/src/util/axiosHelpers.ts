import axios, {type AxiosInstance } from "axios";
import { appConfig } from "../config";
import { csrfAccessToken, csrfRefreshToken } from "./cookieHandlers";

export const protectedInstance: AxiosInstance = axios.create({
    baseURL: appConfig.API_URL,
    timeout: 10000,
    withCredentials: true,
    headers: {
        "X-CSRF-TOKEN": csrfAccessToken()
    }
})

export const publicInstance: AxiosInstance = axios.create({
    baseURL: appConfig.API_URL,
    withCredentials: true,
    timeout: 10000
})

protectedInstance.interceptors.request.use((config) => {
    const newCSRFAccessToken = csrfAccessToken()
    if (newCSRFAccessToken){
        config.headers["X-CSRF-TOKEN"] = newCSRFAccessToken
    }

    return config
})

protectedInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if ([401].includes(error.response?.status) && !originalRequest._retry){
            originalRequest._retry = true;
            try{
                await axios.post(`${appConfig.API_URL}/auth/refresh`, {}, {
                    withCredentials: true,
                    headers: {
                        "X-CSRF-TOKEN": csrfRefreshToken()
                    }
                })
                console.log("Refreshing session...")
                const newAccessToken = csrfAccessToken()
                originalRequest.headers["X-CSRF-TOKEN"] = newAccessToken
                return protectedInstance(originalRequest)
            }catch(refreshError){
                console.warn("Session expired. Logging out...", refreshError)
                window.location.href = '/login-email'
            }
        }
        return Promise.reject(error)
    }
)