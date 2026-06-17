export const appConfig = {
    API_URL: process.env.EXPO_PUBLIC_API_URL 
}

if (!appConfig.API_URL) {
        throw new Error("WARNING: Api url is not defined")
}
