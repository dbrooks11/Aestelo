import { Tabs } from "expo-router";
import Ionicons from '@expo/vector-icons/Ionicons';
import AntDesign from '@expo/vector-icons/AntDesign';
import Feather from '@expo/vector-icons/Feather';


export default function TabLayout() {
    return (
        <Tabs
            screenOptions={{
                headerShadowVisible: false,
                tabBarActiveTintColor: "#BF133C",
                headerStyle: {
                    backgroundColor: "#0F0E0E"
                },
                tabBarStyle: {
                    backgroundColor: "#0F0E0E"
                }
            }}
        >
            <Tabs.Screen
                name="index"
                options={{
                    title: "Home",
                    tabBarIcon: ({color, focused}) => (
                        <Ionicons name={focused ? 'home-sharp' : 'home-outline'} color={color} size={24}/>
                    )
                }}            
            />
            <Tabs.Screen
                name="create"
                options={{
                    tabBarIcon: ({ color, focused }) => (
                    <AntDesign name={focused ? 'plus-circle': 'plus'} color={color} size={24}/>
                )}}
            />
            <Tabs.Screen
                name="profile"
                options={{
                    title: "Profile",
                    tabBarIcon: ({ color, focused }) => (
                        <Feather name={'user'} color={color} size={24}/>
                    )
                }}
            />
        </Tabs>
    );
}