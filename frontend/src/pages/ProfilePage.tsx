
import {useEffect, type JSX, useState} from 'react'
import { protectedInstance } from '../util/axios_api_helpers'
import ProfileHeader from '../components/Profile/ProfileHeader'
import ProfileInfo from '../components/Profile/ProfileInfo'
import ProfileTabs from '../components/Profile/ProfileTabs'
import myProfilePic from '../assets/my_profile_pic.jpg'
import defaultProfilePic from "../assets/default_profile_pic.png"
import type { AxiosResponse } from 'axios'

type ProfileData = {
  id: string,
  profile_photo: string,
  username: string,
  banner_theme: string,
  bio: string,
  instagram: string | undefined,
  tiktok: string | undefined,
  twitter_x: string | undefined,
  facebook: string | undefined,

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

export default function ProfilePage(): JSX.Element {

  const [profileData, setProfileData] = useState<ProfileData | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>("")

  useEffect(() => {
    const profile = async () => {
      try{
        const response: AxiosResponse = await protectedInstance.get('/profile/me')
        const data = response.data

        if(response.status === 200){
          setProfileData(data.my_profile)
          setIsLoading(false)
        }

      }catch(error){
        console.log('failed to fetch profile')
        // AxisErrorHelper(error, setError, "Profile")
        
      }
    }

    profile()
  }, []);
    
  

  return (
    <>
      {!isLoading ? <main className='flex flex-col items-center h-full relative'>
        {error ? error : null}
        <ProfileHeader username = {profileData?.username} follower_count={profileData?.follower_count}/>
        <img src={myProfilePic} className='absolute z-10 aspect-3/1 mask-b-from-65% mask-b-to-80% object-cover w-full pointer-events-none'></img>
        <ProfileInfo 
          profile_pic_url={profileData?.profile_photo ? profileData.profile_photo : myProfilePic} //todo: default icon is temporary (remove it since it has liscense)
          follower_count={profileData?.follower_count ? profileData.follower_count : 0}
          following_count={profileData?.following_count ? profileData.following_count : 0}
          username= {profileData?.username}
          bio = {profileData?.bio ? profileData.bio : "HELLO I AM A FIAMOUS TIKTOKERhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"}
          post_count={profileData?.post_count ? profileData.post_count : 0}
          visit_count={profileData?.visit_count ? profileData.visit_count : 0}
          instagram = {profileData?.instagram ? profileData.instagram : undefined}
          tiktok = {profileData?.tiktok ? profileData.tiktok : undefined}
          twitter_x = {profileData?.twitter_x ? profileData.twitter_x : undefined}
          facebook = {profileData?.facebook ? profileData.facebook : undefined}
        />
        <ProfileTabs/>
      </main>: "Loading Profile..."}
    </>
  )
}
