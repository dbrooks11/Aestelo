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
        // Add CSRF token for state-changing methods
        if (['post', 'put', 'patch', 'delete'].includes(config.method || '')) {
            const csrfToken: string | undefined = csrfAccessToken()
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
                console.log('token expired, refreshing...')

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
                console.error('Token refresh failed:', refreshErr)
                window.location.href = '/login-email'
                return Promise.reject(refreshErr)
            }
        }else{
            console.log('Error')
            window.location.href = '/login-email'  
        }
        return Promise.reject(error);
    }  
)


//axios error handlers

export function AxisErrorHelper(error: AxiosError | unknown, setError: (err: string | null) => void, fallbackErrorName: string): void{
    const axiosError = error as AxiosError<{ error?: string, message?: string }>
                
    if (axiosError.response) {
        // Server responded with error
        const errorMessage = axiosError.response.data?.error || axiosError.response.data?.message || fallbackErrorName
        setError(errorMessage)
        console.error(`${fallbackErrorName} error:`, errorMessage)
    } else if (axiosError.request) {
        // Request made but no response
        setError('No response from server. Please try again.')
        console.error('No response:', axiosError.request)
    } else {
        // Something else happened
        setError('An error occurred. Please try again.')
        console.error('Error:', axiosError.message)
    }
}


export function AxisErrorHelperConsoleOnly(error: AxiosError | unknown, fallbackErrorName: string): void{
    const axiosError = error as AxiosError<{ error?: string, message?: string }>
                
    if (axiosError.response) {
        // Server responded with error
        const errorMessage = axiosError.response.data?.error || axiosError.response.data?.message || fallbackErrorName
        console.error(`${fallbackErrorName} error:`, errorMessage)
    } else if (axiosError.request) {
        // Request made but no response
        console.error('No response:', axiosError.request)
    } else {
        // Something else happened
        console.error('Error:', axiosError.message)
    }
}
