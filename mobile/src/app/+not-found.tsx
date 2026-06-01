import { Link, Stack } from "expo-router";
import { View, Text } from "react-native";



export default function NotFoundScreen() {
    return (
        <>
            <Stack.Screen options={{ title: "Oops, not found!" }}/>
            <View>
            </View>
        </>
    )
}