import heic2any from "heic2any";
import imageCompression from "browser-image-compression";


export const processImageForPreview = async (file: File) => {
  let imageToCompress = file;

  if (file.type === "image/heic" || file.name.toLowerCase().endsWith(".heic")) {
    const convertedBlob: Blob | Array<Blob> = await heic2any({
      blob: file,
      toType: "image/jpeg",
      quality: 0.7, 
    });
    // @ts-expect-error: Blob converion, param is file
    imageToCompress = Array.isArray(convertedBlob) ? convertedBlob[0] : convertedBlob;
  }

  const options = {
    maxSizeMB: 0.4,         
    maxWidthOrHeight: 1024, 
    useWebWorker: true,     
    fileType: "image/jpeg"
  };

  try {
    const compressedBlob = await imageCompression(imageToCompress, options);
    
    return URL.createObjectURL(compressedBlob) 
    
  } catch (error) {
    console.error("Compression failed", error);
  }
};


export const fileCompressionForPreview = (filesList: FileList | null, setIsLoading: (value: boolean) => void, 
    setPreviewPhotos: (value: Array<string | undefined>) => void) => {
        let createdUrls: Array<string | undefined> = []; 
        let isActive: boolean = true; 

        const handleFileChange = async () => {
            if (!filesList || filesList.length === 0) return;

            setIsLoading(true);
            
            try {
                const files: Array<File> = Array.from(filesList);
                
                const urls: Array<string | undefined> = await Promise.all(
                    files.map(file => processImageForPreview(file))
                );

                if (isActive) {
                  createdUrls = urls;
                  // @ts-expect-error: type is already infered by value
                    setPreviewPhotos((prev) => {
                      return [...prev, ...urls]
                        
                    })
                    setIsLoading(false);
                } else {
                    urls.forEach((url) => {
                        if(url) URL.revokeObjectURL(url)
                    });
                }
            } catch (error) {
                console.error(error);
                if (isActive) setIsLoading(false);
            }
        }

        handleFileChange();

        return () => {
            isActive = false; 
            if (createdUrls.length > 0) {
                createdUrls.forEach(url => {if(url) URL.revokeObjectURL(url)});
            }
        }
    }