import axios from 'axios';
import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { appConfig } from './api';
import { router } from 'expo-router';

export const publicInstance = axios.create({
    withCredentials: true,
    baseURL: appConfig.API_URL,
    timeout: 5000
})

export const protectedInstance = axios.create({
    baseURL: appConfig.API_URL,
    withCredentials: true,
    timeout: 5000
});


protectedInstance.interceptors.request.use(async (config) => {
    if (Platform.OS !== 'web') {
        try {
            const token: string | null = await SecureStore.getItemAsync('session');
            const csrfToken: string | null = await SecureStore.getItemAsync('csrfToken');
            if (token && csrfToken) {
                config.headers['Cookie'] = `csrftoken=${csrfToken}; session=${token};`;
                config.headers['x-csrf-token'] = csrfToken;
            }
        } catch (error) {
            console.error("Could not grab tokens from SecureStore", error)
        }
    }

    return config
});

protectedInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (Platform.OS !== 'web') {
            if (error.response?.status === 401) {
                try {
                    await SecureStore.deleteItemAsync('session');
                    console.log("rerouting to login")
                    router.replace('/login');
                } catch (error) {
                    console.log('Failed to remove session from store')
                }
            }

            if (error.response?.status === 403) {
                try {
                    const csrfResponse = await publicInstance.get('/auth/csrf');
                    const token: string | undefined = csrfResponse.data;

                    if (token) {
                        await SecureStore.setItemAsync('csrfToken', token);
                    }
                } catch (error) {
                    console.error('Failed to set CSRF token', error)
                }   
            }
        }   
        return Promise.reject(error);
    }
)