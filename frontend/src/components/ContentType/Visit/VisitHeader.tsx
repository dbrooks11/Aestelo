import { type JSX } from "react";
import ContentHeader from "../ContentHeader";


export default function VisitHeader({username}): JSX.Element{
    return(
        <ContentHeader>
            <img></img>
            <span>{username}</span>
        </ContentHeader>
    )
}