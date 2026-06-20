import { useTheme } from "@/hooks/use-theme";
import { Text, StyleSheet, Pressable } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";


export default function Index() {

  const { toggleTheme } = useTheme();

  return (
    <SafeAreaView style={styles.container}>
      <Text>Edit src/app/index.tsx to edit this screen.</Text>
      <Pressable
        onPress={toggleTheme}
      >
        <Text className="text-primary">Toggling theme</Text>
      </Pressable>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});
