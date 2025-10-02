from exstensions import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean)


#todo: Come back to mapbox and google place id. 
#todo: check format of altitude
#todo: allow multiple photos of location
#todo: 

#TODO: Sponsered locations
#same stuff as regular but have website, price range, parking avalibality, etc
#make key, value pairs for business locations (supabase has exstension for key,val pairs)
# Ex. key (opening hours, wifi avaliable, etc)

#Get metadata from pics
class LocationMetaData(db.Model):
    metadata_id = Column(BigInteger, primary_key=True)
    longitude = Column(String, default=f'{'0.0':.6f}')
    lagitude = Column(String, default=f'{'0.0':.6f}')
    is_long_lat = Column(Boolean) #if place where picture is taken provides the long and late properly, 
                                  #skips Locations details besides basics for post like desciption, name, tags, etc
    altitude = Column(Float, default=0.0)
    created_on = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'))
    verified_status = Column(String(8)) #Will either be pending, verified, or rejected


# Want Exact locations
class LocationCoreData(db.Model):
    location_id = Column(BigInteger, primary_key=True)
    name = Column(String(150))
    google_place_id = Column(BigInteger, default=0)
    mapbox_place_id = Column(BigInteger, default=0)
    metadata_id = Column(BigInteger, ForeignKey('location_meta_data.id'), nullable=False)
    id = Column(BigInteger, ForeignKey('user.id'), nullable=False)



#For businesses mainly
class LocationDetails(db.Model):
    details_id = Column(BigInteger, primary_key=True)
    description = Column(String(200), default='')
    address_line1 = Column(String(50))
    address_line2 = Column(String(20))
    city = Column(String(30))
    state = Column(String(30))
    postal_code = Column(Integer)
    accessibility = Column(Boolean, default=False) #is it accessible to people who are handicapped. True = yes, False = no
    location_id = Column(BigInteger, ForeignKey('location_core_data.id'), nullable=False)



#todo: make another business location model






