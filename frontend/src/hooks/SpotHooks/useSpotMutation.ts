import { useQueryClient } from "@tanstack/react-query"

/* eslint-disable @typescript-eslint/no-explicit-any */
export const useSpotMutation = () => {
    const queryClient = useQueryClient()

    const updateSpotInCache = (spotId: number, newData: object) => {
        queryClient.setQueriesData({queryKey: ['mySpots']}, (oldData: any) => {
            if(!oldData) return oldData

            return {
                ...oldData,
                pages: oldData.pages.map((page: any) => ({
                    ...page,
                    spots: page.spots.map((spot: any) => {
                        if(spot.id === spotId){
                            return {
                                ...spot,
                                ...newData
                            }
                        }
                        return spot
                    })
                }))
            }
        })  
    }

    const updateAllSpotsInCache = (newData: object) => {
        queryClient.setQueriesData({queryKey: ['mySpots']}, (oldData: any) => {
            if(!oldData) return oldData

            return {
                ...oldData,
                pages: oldData.pages.map((page: any) => ({
                    ...page,
                    spots: page.spots.map((spot: any) => {
                        return {
                            ...spot,
                            ...newData
                        }
                    })
                }))
            }
        })  
    }

    return {updateSpotInCache, updateAllSpotsInCache}
}