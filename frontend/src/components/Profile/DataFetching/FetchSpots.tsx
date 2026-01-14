import { type JSX } from "react";
import { useInfiniteQuery} from '@tanstack/react-query'
import { protectedInstance } from "../../../util/axios_api_helpers";
import Spot from "../../Spot/Spot";

const fetchSpots = async({pageParam = 1}) => {
  const response = await protectedInstance.get(`/spot/me?page=${pageParam}`)
  return response.data
}


export default function FetchSpots(): JSX.Element{

    // To query SPOTS
  const {data, fetchNextPage, hasNextPage, isFetchingNextPage} = useInfiniteQuery(
    {
      queryKey: ['mySpots'],
      queryFn: fetchSpots,
      getNextPageParam: (page) => {
        if(page.current_page < page.total_pages){
          return page.current_page + 1
        }
      },
      initialPageParam: 1
    }
  )

    return(
        <section>
            {data?.pages.map((page) => (
              page.spots.map((spot) => {
                return (
                  <Spot
                    key={spot.id}
                    spot={spot}
                  />
                )
              })
            ))}
        </section>
    )
}