import { View, Text } from "react-native";
import { useProfile } from "@/hooks/use-profile";
import { StyleSheet } from "react-native";
import { useTheme } from "@/hooks/use-theme";
import { Image } from "expo-image";

export default function ProfileHeader() {
    const { data } = useProfile();
    const { colors} = useTheme();

    return (
        <View style={[styles.container, {backgroundColor: colors.background}]}>
            <View style={styles.infoContainer}>
                <Image
                    style={styles.avatar}
                    source={data?.avatar} 
                />
                <Text
                    style={[{color: colors.textPrimary, fontWeight: '600'}]}
                >
                    {data?.auth.username}
                </Text>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        position: 'sticky',
        display: 'flex',
        height: 36
    },
    infoContainer: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 4
    },
    avatar: {
        height: 32,
        width: 32,
        borderRadius: 16,
        overflow: 'hidden'
    }
})