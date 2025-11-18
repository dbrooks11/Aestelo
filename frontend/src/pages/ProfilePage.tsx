
import {useEffect, type JSX, useState, type Dispatch, type SetStateAction} from 'react'
import { AxisErrorHelper, protectedInstance } from '../util/axios_api_helpers'
import ProfileBanner from '../components/Profile/ProfileBanner'
import ProfileInfo from '../components/Profile/ProfileInfo'
import ProfileStats from '../components/Profile/ProfileStats'
import defaultProfilePic from "../assets/default_profile_pic.png"
import type { AxiosResponse } from 'axios'

type ProfileData = {
  id: string,
  profile_photo: string,
  username: string,
  banner_theme: string,
  bio: string,
  instagram: string,
  tiktok: string,
  twitter: string,
  facebook: string,

  is_verified_instagram: boolean,
  is_verified_tiktok: boolean,
  is_verified_twitter_x: boolean,
  is_verified_facebook: boolean,
  
  is_business_account: boolean,
  is_prem_account: boolean,
  show_online_status: boolean,
  is_private: boolean,

  follower_count: number,
  following_count: number,
  post_count: number,
  visit_count: number,

  profile_created_at: Date
  
}

export default function ProfilePage({setGlobalErrors}: {setGlobalErrors: Dispatch<SetStateAction<number>>}): JSX.Element {

  const [profileData, setProfileData] = useState<ProfileData | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>("")

  useEffect(() => {
    const profile = async () => {
      try{
        const response: AxiosResponse = await protectedInstance.get('/profile/me')
        const data = response.data

        if(response.status in [200,201,204]){
          setProfileData(data.my_profile)
          console.log(profileData)
        }else{
          setGlobalErrors(response.status)
        }

      }catch(error){
        AxisErrorHelper(error, setError, "Profile")
        
      }
      finally{
        setIsLoading(false)
      }

    
    }

    profile()
  }, []);
    
  

  return (
    <>
    {!isLoading ? <main>
      {error ? error : null}
      <ProfileBanner/>
      <ProfileInfo 
        profile_pic_url={profileData?.profile_photo ? profileData.profile_photo : defaultProfilePic} //todo: default icon is temporary (remove it since it has liscense)
        follower_count={profileData?.follower_count ? profileData.follower_count : 0}
        following_count={profileData?.following_count ? profileData.following_count : 0}
        username= {profileData?.username}
        bio = {profileData?.bio ? profileData.bio : "HELLO I AM A FIAMOUS TIKTOKER"}
      />
      <ProfileStats
        post_count={profileData?.post_count}
        visit_count={profileData?.visit_count}
      />
    </main>: "Loading Profile..."}
    </>
  )
}
