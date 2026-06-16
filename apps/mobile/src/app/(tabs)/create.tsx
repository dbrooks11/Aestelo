import { Text, View, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import ImageViewer from "@/components/createTab/ImageViewer";
import Button from "@/components/createTab/Button";
import * as ImagePicker from 'expo-image-picker';

import { useState } from "react";

const PlaceholderImage = require('@/assets/images/tutorial-web.png');

export default function CreateScreen() {

    const [selectedImage, setSelectedImage] = useState<string | undefined>(undefined)

    const pickImageAsync = async () => {
        const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ['images'],
        allowsEditing: true,
        allowsMultipleSelection: false,
        quality: 1
        });

        if (!result.canceled) {
            console.log(result)

            setSelectedImage(result.assets[0].uri)

            const imageArray: Array<string> = []

            result.assets.forEach((image) => {
                console.log(image.mimeType)
                console.log(image.fileName)
                console.log(image.exif)
                console.log(image.fileSize)

                imageArray.push(image.uri)
            })
        } else {
            alert('No images selected')
        }
    }
    
    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.imageContainer}>
                <ImageViewer imgSource={PlaceholderImage} selectedImage={selectedImage} />
            </View>
            <View style={styles.footerContainer}>
                <Button onPress={pickImageAsync} label="Choose a photo"/>
                <Button onPress={pickImageAsync} label="Use this one"/>
            </View>
        </SafeAreaView>
    )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },
  imageContainer: {
    flex: 1,
    paddingTop: 8,
  },
  footerContainer: {
    flex: 1 / 3,
    alignItems: 'center',
  },
});