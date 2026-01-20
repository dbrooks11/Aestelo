import { useCallback, useRef, useState, type JSX } from "react";
import { useInfiniteQuery} from '@tanstack/react-query'
import { protectedInstance } from "../../../util/axios_api_helpers";
import Spot from "../../Spot/Spot";
import SpotSimple from "../../Spot/SpotSimple/SpotSimple";
import Modal from "../../Modal";

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

  return(
    /* eslint-disable @typescript-eslint/no-explicit-any */
      <section className="md:m-2 flex flex-col">
        {/* 1. THE GRID (Only Thumbnails) */}
        <div className="grid md:grid-cols-4 grid-cols-3 md:gap-2 gap-0.5 relative">
          {data?.pages.map((page) =>
            page.spots.map((spot: any) => (
              <SpotSimple
                key={spot.id}
                spot={spot}
                onClick={() => setSelectedSpot(spot)}
                className="w-full aspect-4/5 hover:scale-102 cursor-pointer transition-transform object-cover rounded-xs overflow-hidden"
              />
            ))
          )}
        </div>

        {/* 2. THE MODAL (Full View Overlay) */}
        <Modal
          closeModal={() => setSelectedSpot(undefined)}
          showModal={selectedSpot ? true : false}
          closeOnBgClick={true}
          className="flex flex-col w-fit h-fit rounded-none bg-none border-none my-16 md:my-20"
          preventDefault={true}
          preventPropagation={true}
        >
        {selectedSpot && (
            <Spot 
                spot={selectedSpot} 
                className={''}
            />
          )}
        </Modal>
        <div 
          ref={observerCallback}
          className="w-full h-5 invisible"
        ></div>
      </section>
  )
}