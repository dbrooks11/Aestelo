import { Pressable, ScrollView, Text, View } from "react-native";
import { useSession } from "@/context/auth-ctx";




export default function ProfileScreen() {
    const { signOut } = useSession();
    
   
    return (
        <View className="mt-30">
            <ScrollView>
                <Pressable onPress={signOut}>
                    <Text className="text-primary">Sign Out Here</Text>
                </Pressable>
            </ScrollView>
        </View>
    )
}