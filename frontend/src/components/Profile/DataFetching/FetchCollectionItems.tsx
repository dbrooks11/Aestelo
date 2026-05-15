import { useCallback, useRef, type JSX } from "react";
import { useInfiniteQuery } from "@tanstack/react-query";
import { protectedInstance } from "../../../util/axiosHelpers";
import SpotCard from "../Cards/SpotCard/SpotCard";


const fetchCollectionItems = async({pageParam = 1, collection_id}:{pageParam:number, collection_id: number}) => {
    const response = await protectedInstance.get(`/collection/${collection_id}/view?page=${pageParam}`)

    return response.data
}

export default function FetchCollectionItems({collection_id}:{collection_id: number}): JSX.Element{

    const observerContainerRef = useRef<IntersectionObserver | null>(null)

    const {data, fetchNextPage, hasNextPage, isFetchingNextPage} = useInfiniteQuery({
        queryKey: ['myCollectionItems', collection_id],
        queryFn: ({pageParam = 1}) => fetchCollectionItems({
            pageParam,
            collection_id
        }),
        getNextPageParam: (page) => {
            if(page.current_page < page.total_pages){
                return page.current_page + 1
            }
            return undefined
        },
        initialPageParam: 1
    })

    const observerCallback = useCallback((node: HTMLDivElement) => {
        if(isFetchingNextPage) return

        if(observerContainerRef.current) observerContainerRef.current.disconnect()
        
            observerContainerRef.current = new IntersectionObserver(entries => {
                if(entries[0].isIntersecting && hasNextPage){
                    fetchNextPage()
                }
            })
        
        if(node && observerContainerRef.current) observerContainerRef.current.observe(node)
    }, [fetchNextPage, hasNextPage, isFetchingNextPage])

    console.log(data?.pages)
    return(
        /* eslint-disable @typescript-eslint/no-explicit-any */
        <div className="grid md:grid-cols-4 grid-cols-3 lg:grid-cols-6 md:gap-2 gap-0.5 md:p-2">
            {data?.pages.map((page) => {
                return page.collection_items.map((item: any) => {
                    return (
                        item.spot && <SpotCard key={item.spot.id} spot={item.spot} className={'text-sm lg:text-[15px]'} onClick={undefined} includeUsername={true}/> 
                    )
                })
            })}
            <div 
                ref={observerCallback}
                className="invisible w-full h-5"
            ></div>  
        </div>
    )
}