import { Stack } from "expo-router";
import { SessionProvider, useSession } from "@/context/authCtx";
import { SplashScreenController } from "@/splash";

export default function RootLayout() {
  return (
    <SessionProvider>
      <SplashScreenController/>
      <RootNavigator/>
    </SessionProvider>
  );
}


function RootNavigator() {
  const { session } = useSession();

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