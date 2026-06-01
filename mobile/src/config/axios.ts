import axios from 'axios';
import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { appConfig } from './api';


export const publicInstance = axios.create({
    baseURL: appConfig.API_URL,
    timeout: 10000
})

export const protectedInstance = axios.create({
    baseURL: appConfig.API_URL,
    withCredentials: true,
    timeout: 10000
});


protectedInstance.interceptors.request.use(async (config) => {
    if (Platform.OS !== 'web') {
        try {
            const token: string | null = await SecureStore.getItemAsync('session');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        } catch (error) {
            console.error("Could not grab token from SecureStore", error)
        }
    }

    return config
})