export function handleNumStats(stat: number) {
    if (stat === 0) return "0"

    const thousand = 1000
    const tenThousand = 10000
    const million = 1000000
    const billion = 1000000000
    const trillion = 1000000000000

    const floorStat = (value: number) => {
        return Math.floor(value * 10) / 10;
    };

        if (stat >= trillion) {
            return floorStat(stat / trillion) + 't'
        } 
        if (stat >= billion) {
            return floorStat(stat / billion) + 'b'
        } 
        if (stat >= million) {
            return floorStat(stat / million) + 'm'
        }
        if(stat >= tenThousand){
            return floorStat(stat / thousand) + 'k'
        }
        
    return stat.toString();
    }