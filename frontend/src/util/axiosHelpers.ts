import axios, {type AxiosInstance } from "axios";
import { appConfig } from "../config";
import { csrfAccessToken } from "./cookieHandlers";


export const protectedInstance: AxiosInstance = axios.create({
    baseURL: appConfig.API_URL,
    timeout: 10000,
    withCredentials: true,
    headers:{
        "X-CSRF-TOKEN": csrfAccessToken()
    }
})

export const publicInstance: AxiosInstance = axios.create({
    baseURL: appConfig.API_URL,
    withCredentials: true,
    timeout: 10000
})