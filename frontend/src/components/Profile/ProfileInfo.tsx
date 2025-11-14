
import type {JSX} from 'react'

type ProfileInfoParams = {
    username: string | undefined,
    profile_pic_url: string | undefined,
    bio: string | undefined,
    following_count: number | undefined,
    follower_count: number | undefined
}

export default function ProfileInfo({username, profile_pic_url, bio, following_count, follower_count}: ProfileInfoParams):JSX.Element {
  return (
     <section className='profile_info'>
        <img src={profile_pic_url} alt="User's Profile Picture" width = "100px"></img>
        <div>
            <div>
                <span>{`Followers: ${follower_count}`}</span> 
                <span>{`Following: ${following_count}`}</span>
            </div>
        </div>
        <h3 role = 'username' aria-label="username">@{username}</h3>
        <p role='bio'>{bio}</p>
     </section>
  )
}
