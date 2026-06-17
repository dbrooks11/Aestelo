import { Pressable, ScrollView, Text, View } from "react-native";
import { useSession } from "@/context/auth-ctx";
import ProfileBanner from "@/components/profile/Banner";




export default function ProfileScreen() {
    const {signOut} = useSession()

    return (
        <View>
            <ScrollView>
                <ProfileBanner/>
            </ScrollView>
        </View>
    )
}