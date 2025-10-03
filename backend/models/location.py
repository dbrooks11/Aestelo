from exstensions import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Integer, Float, Text, DateTime, Boolean)
from sqlalchemy.dialects.postgresql import UUID
from .schema_types import *

#todo: Come back to mapbox and google place id. 
#todo: check format of altitude
#todo: allow multiple photos of location
#todo: do business locations
#todo: 

#TODO: Sponsered locations
#same stuff as regular but have website, price range, parking avalibality, etc
#make key, value pairs for business locations (supabase has exstension for key,val pairs)
# Ex. key (opening hours, wifi avaliable, etc)


#User uses builtin camera function in app so meta_data_id cant be changed
#Get meta_data_id from pics


class Location(db.Model):
    __tablename__ = "location"
    __table_args__ = {'schema': location_schema} 
    post_id = Column(UUID(as_uuid=True), ForeignKey(f'{post_schema}.post.post_id'))
    visit_id = Column(UUID(as_uuid=True), ForeignKey(f'{visit_schema}.visit.visit_id'))
    location_coredata = relationship('LocationCoreData', backref='location', lazy=True)
    business_location_details = relationship('BusinessLocationDetails', backref='location', lazy=True) #will be handled later
    is_visit = Column(Boolean, default=False) #if its a visit, itll refernce the visit id
        
    meta_data_id = Column(UUID(as_uuid=True), primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    is_long_lat = Column(Boolean) #if place where picture is taken provides the long and late properly, 
                                  #skips Locations details besides basics for post like desciption, name, tags, etc
    altitude = Column(Float, default=0.0)

    created_on = Column(DateTime, default= datetime.now(timezone.utc).strftime('%b %d, %Y'))
    verified_status = Column(String(8), default='pending') #Will either be pending, verified, or rejected to verify the location
    
    def to_dict(self):
        return {
            'post_id': self.post_id,
            'visit_id': self.visit_id, 
            'is_visit': self.is_visit,
            'meta_data_id': self.meta_data_id,
            'longitude': self.longitude,
            'lagitude': self.latitude,
            'is_long_lat': self.is_long_lat,
            'altitude': self.altitude,
            'created_on': self.created_on,
            'verified_status': self.verified_status
    }

# Want Exact locations
class LocationCoreData(db.Model):
    __tablename__ = "location_core_data"
    __table_args__ = {'schema': location_coredata_schema} 
    meta_data_id = Column(UUID(as_uuid=True), ForeignKey(f'{location_schema}.location.meta_data_id'), primary_key=True, nullable=False)
    mapbox_place_id = Column(BigInteger, default=0)
    name = Column(String(150))

    def to_dict(self):
        return {
            'meta_data_id': self.meta_data_id,
            'mapbox_place_id': self.mapbox_place_id,
            'name': self.name
    }



#For businesses mainly
class BusinessLocationDetails(db.Model):
    __tablename__ = "businesss_location_details"
    __table_args__ = {'schema': business_location_details_schema} 
    meta_data_id = Column(UUID(as_uuid=True), ForeignKey(f'{location_schema}.location.meta_data_id'), primary_key=True)
    description = Column(String(200), default='')
    address_line1 = Column(String(50))
    address_line2 = Column(String(20))
    city = Column(String(30))
    state = Column(String(30))
    postal_code = Column(Integer)
    
    def to_dict(self):
        return {
            'meta_data_id': self.meta_data_id,
            'description': self.description,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code
    }



#todo: make another business location model






