import { useProfile } from "@/hooks/use-profile";
import { Image } from "expo-image";
import { View } from "react-native";
import { StyleSheet } from "react-native";


export default function ProfileBanner() {
    const { data } = useProfile();

    return (
        <View className="flex">
            <Image className="h-64" source={data?.banner} />
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        display: 'flex'
    },
    banner: {
        width: 'auto',
        height: 260
    }
})