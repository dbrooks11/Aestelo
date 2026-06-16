import { useQuery } from "@tanstack/react-query";
import { protectedInstance } from "@/config/axios";
import { useTheme } from "./use-theme";
import defaultAvatar from '@/assets/profile/default-avatar.svg';
import defaultBannerLight from '@/assets/profile/default-banner-light.svg';
import defaultBannerDark from '@/assets/profile/default-banner-dark-converted-from-svg.webp';


export type Username = ProfileDataType['auth']['username']
export type ProfileDataType = {
  id: string,
  avatar: string | undefined
  banner: string,
  auth: {'username': string}
  bio: string | undefined,

  followerCount: number,
  followingCount: number,
  spotCount: number,
  visitCount: number,

  createdAt: Date 
}


export function useProfile() {
    const { theme } = useTheme();

    return useQuery<ProfileDataType>({
        queryKey: ['profile', theme],
        queryFn: async () => {
            const response = await protectedInstance.get('/profile');
            let profile = response.data
            
            const defaultBanner = theme === 'light' ? defaultBannerLight : defaultBannerDark
            profile = {
                ...profile,
                avatar: profile.avatar ? {uri: profile.avatar} : defaultAvatar,
                banner: profile.banner ? {uri: profile.banner } : defaultBanner
            } 
            
            return profile
        }
    })
}