import { useCallback, useRef, useState, type JSX } from "react";
import { useInfiniteQuery} from '@tanstack/react-query'
import { protectedInstance } from "../../../util/axios_api_helpers";
import Spot from "../../Spot/Spot";
import SpotSimple from "../../Spot/SpotSimple/SpotSimple";
import { AnimatePresence, motion } from "framer-motion";

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

  const handleSpotClick = () => {

  }

  return(
      <section className="md:m-2 flex flex-col">
        {/* 1. THE GRID (Only Thumbnails) */}
        <div className="grid md:grid-cols-4 grid-cols-3 md:gap-2 gap-1 relative">
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
        <AnimatePresence>
        {selectedSpot && (
          <div className="fixed inset-0 z-50 flex items-center justify-center">
            
            {/* Backdrop (Click to close) */}
            <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setSelectedSpot(undefined)}
                className="absolute inset-0 bg-black/20 backdrop-blur-xs"
            />

            {/* The Full Spot Card */}
            <motion.div 
                layoutId={`spot-${selectedSpot.id}`}
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="relative z-10"
            >
                <Spot 
                    spot={selectedSpot} 
                    className={''}
                />
            </motion.div>
          </div>
          )}
        </AnimatePresence>
        <div 
          ref={observerCallback}
          className="w-full h-5 invisible"
        ></div>
      </section>
  )
}