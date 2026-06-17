import { Stack } from "expo-router";
import { SessionProvider, useSession } from "@/context/auth-ctx";
import { SplashScreenController } from "@/splash";
import { Platform} from "react-native";
import { publicInstance } from "@/config/axios";
import { useEffect } from "react";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import * as SecureStore from 'expo-secure-store';
import { ThemeProvider } from "@/context/theme-ctx";
import { useTheme } from "@/hooks/use-theme";

import '../../../global.css';


const queryClient = new QueryClient();

export default function RootLayout() {

  useEffect(() => {
    const setCsrfToken = async () => {
      try {
        if (Platform.OS !== 'web') {
          const csrfResponse = await publicInstance.get('/auth/csrf');
          const token: string | undefined = csrfResponse.data;

          if (token) {
            await SecureStore.setItemAsync('csrfToken', token)
          }
        }
      } catch (error) {
        console.error('Failed to set CSRF Token', error)
      }
    }
    setCsrfToken()
  }, []);
  

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <SessionProvider>
          <SplashScreenController/>
          <RootNavigator />
        </SessionProvider>
      </ThemeProvider>
    </QueryClientProvider>
    
  );
}


function RootNavigator() {
  const { session } = useSession();
  const { colors } = useTheme();

  return (
    <Stack>
      <Stack.Protected guard={!!session}>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      </Stack.Protected>
      
      <Stack.Protected guard={!session}>
        <Stack.Screen name="login" />
      </Stack.Protected>
    </Stack>
  );
}