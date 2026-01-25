import { useCallback, useRef, useState, type JSX } from "react";
import { protectedInstance } from "../../../util/axios_api_helpers";
import { useInfiniteQuery } from "@tanstack/react-query";
import CollectionCard from "../Cards/CollectionCard/CollectionCard";
import AddCollectionCard from "../Cards/CollectionCard/AddCollectionCard";
import FetchCollectionItems from "./FetchCollectionItems";

const fetchCollections = async({pageParam = 1}) => {
    const response = await protectedInstance.get(`/collection/me?page=${pageParam}`)
    return response.data
}

export default function FetchCollections(): JSX.Element{

    const observerContainerRef = useRef<IntersectionObserver | null>(null)
    const [viewCollection, setViewCollection] = useState<number | undefined>(undefined)

    const {data, fetchNextPage, hasNextPage, isFetchingNextPage} = useInfiniteQuery({
        queryKey: ['myCollections'],
        queryFn: fetchCollections,
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

    return(
        /* eslint-disable @typescript-eslint/no-explicit-any */
        <>
            
            {viewCollection === undefined ? <div className="gap-1 md:gap-2 grid grid-cols-3 md:grid-cols-4 xl:grid-cols-6 p-1 md:p-4">
                <AddCollectionCard/>
                {data?.pages.map((page) => {
                    return page.collections.map((collection: any) => {
                        return (
                            <CollectionCard 
                            key={collection.id}
                            collection={collection}
                            viewCollection={viewCollection}
                            setViewCollection={setViewCollection}/>
                        )
                    })
                })}
            </div>: <FetchCollectionItems collection_id={viewCollection}/>}
            <div 
                ref={observerCallback}
                className="invisible w-full h-5"
            ></div>
        </>
    )
}