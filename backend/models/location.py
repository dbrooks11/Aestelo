from exstensions import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import (Column, ForeignKey, BigInteger, 
                        String, Float, DateTime, Boolean, Index)
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


#user uses builtin camera function in app so location_id cant be changed
#Get location_id from pics


class Location(db.Model):
    __tablename__ = "location"
    __table_args__ = (Index('idx_location_coords', 'latitude', 'longitude'),
                      {'schema': location_schema})
    
    post_media_id = Column(BigInteger, ForeignKey(f'{post_media_schema}.post_media.post_media_id'), index=True, nullable=True)
    visit_media_id = Column(BigInteger, ForeignKey(f'{visit_media_schema}.visit_media.visit_media_id'), index=True, nullable=True)
    business_location_details = relationship('BusinessLocationDetails', backref='location', lazy=True) #will be handled later
   
        
    location_id = Column(BigInteger, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    altitude = Column(Float)


    created_on = Column(DateTime, default= datetime.now(timezone.utc))

    
    def to_dict(self):
        return {
            "post_id": self.post_id,
            "visit_id": self.visit_id, 
            "location_id": self.location_id,
            "is_visit": self.is_visit,
            "longitude": self.longitude,
            "latitude": self.latitude,  # fixed typo: lagitude → latitude
            "is_long_lat": self.is_long_lat,
            "altitude": self.altitude,
            "created_on": self.created_on,
            "verified_status": self.verified_status
    }

    def save(self):
        db.session.add(self)
        db.session.commit()



#For businesses mainly
class BusinessLocationDetails(db.Model):
    __tablename__ = "businesss_location_details"
    __table_args__ = {'schema': business_location_details_schema} 

    location_id = Column(BigInteger, ForeignKey(f'{location_schema}.location.location_id'), primary_key=True)
    description = Column(String(200), default='')
    address_line1 = Column(String(50))
    address_line2 = Column(String(20))
    city = Column(String(30))
    state = Column(String(30))
    postal_code = Column(String(10))
    
    def to_dict(self):
        return {
            'location_id': self.location_id,
            'description': self.description,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code
    }

    def save(self):
        db.session.add(self)
        db.session.commit()



#todo: make another business location model






