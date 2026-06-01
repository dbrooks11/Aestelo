import { ImageSourcePropType, StyleSheet } from "react-native";
import { Image } from "expo-image";

type props = {
    imgSource: ImageSourcePropType;
    selectedImage?: string;
}


export default function ImageViewer(props: props) {
    const imageSource = props.selectedImage ? props.selectedImage : props.imgSource

    return (
        <Image source={imageSource} style={styles.image} />
    )
}

const styles = StyleSheet.create({
  image: {
    width: 320,
    height: 400,
    borderRadius: 18,
  },
});