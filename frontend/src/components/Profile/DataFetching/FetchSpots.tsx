import { useCallback, useRef, useState, type JSX } from "react";
import { useInfiniteQuery} from '@tanstack/react-query'
import { protectedInstance } from "../../../util/axiosHelpers";
import Spot from "../../ContentType/Spot/Spot";
import Modal from "../../Modal";
import SpotCard from "../Cards/SpotCard/SpotCard";

const fetchSpots = async({pageParam = 1}) => {
  const response = await protectedInstance.get(`/spot/me?page=${pageParam}`)
  return response.data
}

export default function FetchSpots(): JSX.Element{

  const observerContainerRef = useRef<IntersectionObserver | null>(null)
  const [selectedSpot, setSelectedSpot] = useState<object | undefined>(undefined)


  const {data, fetchNextPage, hasNextPage, isFetchingNextPage} = useInfiniteQuery(
    {
      queryKey: ['mySpots'],
      queryFn: fetchSpots,
      getNextPageParam: (page) => {
        if(page.current_page < page.total_pages){
          return page.current_page + 1
        }
        return undefined
      },
      initialPageParam: 1
    }
  )

  const observerCallback = useCallback((node: HTMLDivElement) => {
    if(isFetchingNextPage) return

    if(observerContainerRef.current) observerContainerRef.current.disconnect()

    
      observerContainerRef.current = new IntersectionObserver(entries => {
        if(entries[0].isIntersecting && hasNextPage){
          fetchNextPage()
        }
      })

    if(node && observerContainerRef.current) observerContainerRef.current.observe(node)
  }, [isFetchingNextPage, hasNextPage, fetchNextPage])
 
  const collections = data?.pages[0]?.collections || []
  

  return(
    /* eslint-disable @typescript-eslint/no-explicit-any */
      <>
        {/* 1. THE GRID (Only Thumbnails) */}
        <div className="gap-0.5 md:gap-1 grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 md:p-2">
          {data?.pages.map((page) =>
            page.spots.map((spot: any) => (
              <SpotCard
                key={spot.id}
                spot={spot}
                onClick={() => setSelectedSpot(spot)}
                includeUsername={undefined}
                className="rounded-xs w-full object-cover aspect-4/5 overflow-hidden md:hover:scale-102 transition-transform cursor-pointer"
              />
            ))
          )}
        </div>

        {/* 2. THE MODAL (Full View Overlay) */}
        <Modal
          closeModal={() => setSelectedSpot(undefined)}
          showModal={selectedSpot ? true : false}
          closeOnBgClick={true}
          className="flex flex-col bg-none my-16 md:my-20 border-none rounded-none w-fit h-fit"
          preventDefault={true}
          preventPropagation={true}
        >
        {selectedSpot && (
            <Spot
                key={selectedSpot.id}
                spot={selectedSpot} 
                collections={collections}
                className={''}
            />
          )}
        </Modal>
        <div 
          ref={observerCallback}
          className="invisible w-full h-5"
        ></div>
      </>
  )
}