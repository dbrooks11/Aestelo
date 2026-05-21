from enum import Enum

class UserRoleEnum(Enum):
    USER = 'User'
    ADMIN = 'Admin'
    MODERATOR = 'Moderator'
    OWNER = 'Owner'

class UploadStatusEnum(Enum):
    PROCESSING = 'Processing'
    FAILED = 'Failed'
    SUCCESS = 'Success'

class MediaTypeEnum(Enum):
    PHOTO = 'Photo'
    VIDEO = 'Video'

class UserGenderEnum(Enum):
    NOT_SPECIFIED = 'Not specfied'
    MALE = 'Male'
    FEMALE = 'Female'
    NON_BINARY = 'Non-Binary'

class LanguagePreferenceEnum(Enum):
    ENGLISH = 'English'
    SPANISH = 'Spanish'

class UserSubscriptionTierEnum(Enum):
    FREE = 'Free'
    PRO = 'Pro'

class UserSubscriptionBillCycleEnum(Enum):
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'