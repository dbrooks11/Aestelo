
import {useEffect, type JSX, useState} from 'react'
import { protectedInstance } from '../util/axiosHelpers'
import DefaultBannerDark from "../assets/default_banner_dark.svg"
import DefaultBannerLight from "../assets/default_banner_light.svg"
import DefaultPhoto from "../assets/default_photo.svg"
import ProfileHeader from '../components/Profile/ProfileHeader'
import ProfileBanner from '../components/Profile/ProfileBanner'
import ProfileInfo from '../components/Profile/ProfileInfo'
import ProfileTabs from '../components/Profile/ProfileTabs'
import EditProfileForm from '../components/Forms/ProfileEditForm'
import type { AxiosResponse } from 'axios'
import ToasterCustom from '../components/Toast'
import { useTheme } from '../context/ThemeContext'
import ProfileLoadingSkeleton from '../components/Skeletons/ProfileSkeleton'

export type ProfileDataType = {
  id: string,
  profile_photo: string | undefined
  profile_banner: string | undefined,
  username: string | undefined,
  banner_theme: string | undefined,
  bio: string | undefined,
  instagram: string | undefined,
  tiktok: string | undefined,
  twitter_x: string | undefined,
  facebook: string | undefined,

  follower_count: number | undefined,
  following_count: number | undefined,
  spot_count: number | undefined,
  visit_count: number | undefined,

  profile_created_at: Date
  
}

export type ProfileDataUseState = ProfileDataType | null


export default function ProfilePage(): JSX.Element {

  const {theme} = useTheme()
  const [profileData, setProfileData] = useState<ProfileDataUseState>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [showModal, setShowModal] = useState<boolean>(false)
  const banner = `${theme === 'light' ? DefaultBannerLight : DefaultBannerDark}`


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
        console.error(error)
        
      }
    }

    profile()
  }, []);

  return (
    <>
      {!isLoading ? <main className='relative flex flex-col items-center h-full'>
        <ProfileHeader 
          username = {profileData?.username} 
          follower_count={profileData?.follower_count}/>
          
        <ProfileBanner profileBanner={profileData?.profile_banner ?? banner}/> 
        <ProfileInfo 
          profile_photo={profileData?.profile_photo ?? DefaultPhoto} 
          follower_count={profileData?.follower_count}
          following_count={profileData?.following_count}
          username= {profileData?.username}
          bio = {profileData?.bio}
          spot_count={profileData?.spot_count}
          visit_count={profileData?.visit_count}
          instagram = {profileData?.instagram}
          tiktok = {profileData?.tiktok}
          twitter_x = {profileData?.twitter_x}
          facebook = {profileData?.facebook}
          setProfileData = {setProfileData}
          profileData = {profileData}
          setShowModal = {setShowModal}
          showModal = {showModal}
        />
        
        <ProfileTabs/>
        <EditProfileForm
          profileBannerUrl={profileData?.profile_banner ?? banner}
          profilePhotoUrl={profileData?.profile_photo ?? DefaultPhoto}  
          username = {profileData?.username} 
          bio = {profileData?.bio}
          setProfileData={setProfileData}
          setShowModal={setShowModal}
          showModal={showModal}
        />
        <ToasterCustom toasterId='profile'/>
      </main>: <ProfileLoadingSkeleton/>}
    </>
  )
}
