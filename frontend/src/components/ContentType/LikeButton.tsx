import { type JSX } from "react";
import { Heart } from "lucide-react";
import ButtonBase from "./ButtonBase";

export default function LikeButton(props): JSX.Element{

    const color = "#d61818"
    const fillColor = "#d61818"

    return(
        <>
            <ButtonBase
                title="Like"
                icon={Heart}
                color={color}
                fillColor={fillColor}

            />
        </>
    )
}