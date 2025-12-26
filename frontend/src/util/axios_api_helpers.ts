import axios, { AxiosError, type AxiosInstance } from "axios";
import { appConfig } from "../config";
import Cookies from 'js-cookie'


//csrf cookie helper functions
export const csrfAccessToken = (): string | undefined =>{
    return Cookies.get('csrf_access_token')
}

export const csrfRefreshToken = (): string | undefined =>{
    return Cookies.get('csrf_refresh_token')
}

//axios instances
export const signupInstance: AxiosInstance = axios.create({
    baseURL: appConfig.API_URL,
    timeout: 10000,
    headers: {'Content-Type': 'application/json'},
    withCredentials: false
})

export const loginInstance: AxiosInstance = axios.create({
    baseURL: appConfig.API_URL,
    timeout: 10000,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true 
})

export const protectedInstance: AxiosInstance = axios.create({
    baseURL: appConfig.API_URL,
    timeout: 10000,
    headers:{'Content-Type': 'application/json'},
    withCredentials: true
})

//axios intercepter
protectedInstance.interceptors.request.use(
    (config) => {

        const isRefreshRequest: boolean | undefined = config.url?.includes('/refresh')
        const csrfToken: string | undefined = isRefreshRequest ? csrfRefreshToken() : csrfAccessToken()

        // Add CSRF token for state-changing methods
        if (['post', 'put', 'patch', 'delete', 'get'].includes(config.method || '')) {
            if (csrfToken) {
                config.headers['X-CSRF-TOKEN'] = csrfToken
            }
        }
        return config
    },
    (error) => Promise.reject(error)
)


protectedInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const {response, config} = error;

        // Handle expired access token
        if (response?.status === 401 && !config.__isRetry) {
            config.__isRetry = true;

            try {

                const refreshToken: string | undefined = csrfRefreshToken();
                if (refreshToken) {
                    await axios.post(`${appConfig.API_URL}/auth/refresh`, {}, {
                        withCredentials: true,
                        headers: {'X-CSRF-TOKEN': refreshToken}
                    })

                    const newCsrfToken: string | undefined = csrfAccessToken()
                    if (newCsrfToken && ['post', 'put', 'patch', 'delete'].includes(config.method || '')) {
                        config.headers['X-CSRF-TOKEN'] = newCsrfToken
                    }
                    return protectedInstance(config);
                }
            } catch (refreshErr) {
                return Promise.reject(refreshErr)
            }
        }
        return Promise.reject(error);
    }  
)


//axios error handlers

export function AxiosErrorHelper(error: AxiosError | unknown): string{
    let errorMessage = "Something went wrong";

    if (axios.isAxiosError(error)) {
        if (error.response) {
            const serverData = error.response.data;
            
            if (serverData && serverData.error) {
                if (Array.isArray(serverData.error)) {
                    errorMessage = serverData.error.join(", ");
                } else if (typeof serverData.error === 'object') {
                     errorMessage = Object.values(serverData.error).join(", ");
                } else {
                    errorMessage = serverData.error;
                }
            }
        } else if (error.request) {
            errorMessage = "Network error. Please check your connection.";
        }
    } else if (error instanceof Error) {
        errorMessage = error.message;
    } else {
        errorMessage = 'An error occured. Please try again.'
    }

    return errorMessage
}


export function AxisErrorHelperConsoleOnly(error: AxiosError | unknown, fallbackErrorName: string): void{
    const axiosError = error as AxiosError<{ error?: string, message?: string }>
                
    if (axiosError.response) {
        // Server responded with error
        const errorMessage = axiosError.response.data?.error || axiosError.response.data?.message || fallbackErrorName
        // console.error(`${fallbackErrorName} error:`, errorMessage)
    } else if (axiosError.request) {
        // Request made but no response
        console.error('No response:', axiosError.request)
    } else {
        // Something else happened
        // console.error('Error:', axiosError.message)
    }
}
