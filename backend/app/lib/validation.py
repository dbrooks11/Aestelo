
import re


class ValidationConfiguration:
    MAX_HEIGHT=2560
    MAX_WIDTH=1440
    QUALITY = 85
    COMPRESSION_IMAGE_TYPE='webp'
    MAX_FILE_SIZE = 10 * 1024 * 1024 
    MAX_NUM_FILES_POST=10
    MAX_NUM_FILES_PROFILE=2

    MAX_POST_MEDIA_COUNT=10
    MIN_POST_MEDIA_COUNT=1
    MAX_POST_HASHTAG_COUNT=20
    MIN_POST_HASHTAG_COUNT=0
    MAX_POST_DESCRIPTION_LENGTH= 250
    MIN_POST_DESCRIPTION_LENGTH=0
    MAX_PROFILE_BIO_LENGTH=150

    EMAIL_BASIC_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$")
    EMAIL_DOUBLE_DOT_PATTERN = re.compile(r"\.\.+")
    EMAIL_BLOCKED_PATTERNS = [
        re.compile(r".*\+.*test.*@.*"),
        re.compile(r".*\+.*spam.*@.*"),
        re.compile(r"^test.*@.*"),
        re.compile(r"^noreply@.*"),
        re.compile(r"^no-reply@.*"),
    ]

    PASSWORD_UPPERCASE_PATTERN = re.compile(r"[A-Z]")
    PASSWORD_LOWERCASE_PATTERN = re.compile(r"[a-z]")
    PASSWORD_DIGIT_PATTERN = re.compile(r"\d")
    PASSWORD_SPECIAL_PATTERN = re.compile(r'[!@#$%^&*(),.?":{}|<>_+=\-\[\]\\\/~`]')
    PASSWORD_COMMON_PATTERN = re.compile(r"(password|123456|qwerty|admin)", re.IGNORECASE)
    PASSWORD_REPEATED_PATTERN = re.compile(r"(.)\1{4,}")
    PASSWORD_SIMPLE_REPEATED_PATTERN = re.compile(r"^(.)\1{11,}$")
    PASSWORD_SEQUENTIAL_PATTERN = re.compile(r"^(012|123|234|345|456|567|678|789|890|abc|bcd|cde)", re.IGNORECASE)
    PASSWORD_KEYBOARD_PATTERN = re.compile(r"^(qwe|asd|zxc)", re.IGNORECASE)

    NAME_WHITESPACE_PATTERN = re.compile(r"\s+")
    NAME_VALID_PATTERN = re.compile(r"^[a-zA-ZÀ-ÿĀ-žА-я\u4e00-\u9fff\u0600-\u06ff\u3040-\u309f\u30a0-\u30ff\s'\-\.]+$")
    NAME_REPEATED_PATTERN = re.compile(r"(.)\1{4,}")

    USERNAME_VALID_PATTERN = re.compile(r'^(?!.*\.$)(?!^\.)[a-z0-9._]+$')

    SLUG_VALID_PATTERN = re.compile(r"^[a-z0-9-]+$")

    PHONE_BASIC_PATTERN = re.compile(r"^[\+]?[0-9\s\-\(\)\.]+$")
    PHONE_DIGITS_PATTERN = re.compile(r"[^\d]")

    EMAIL_BLOCKED_DOMAINS = [
        "10minutemail.com",
        "tempmail.org",
        "guerrillamail.com",
        "mailinator.com",
        "throwaway.email",
        "temp-mail.org",
        "yopmail.com",
        "maildrop.cc",
        "dispostable.com",
        "trashmail.com",
        "fake-mail.cf",
        "tempmail.net",
    ]

    COMMON_PASSWORDS = {
        "password",
        "password123",
        "123456789",
        "qwertyuiop",
        "administrator",
        "welcome123",
        "password1234",
        "letmein123",
        "admin123456",
        "password12345",
    }

    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 128
    PASSWORD_STRONG_LENGTH = 12
    PASSWORD_VERY_STRONG_LENGTH = 20

    PASSWORD_SCORE_STRONG = 7
    PASSWORD_SCORE_MEDIUM = 5

    PHONE_MIN_DIGITS = 7
    PHONE_MAX_DIGITS = 15

    EMAIL_MAX_LENGTH = 254
    EMAIL_MIN_LENGTH = 5
    EMAIL_LOCAL_PART_MAX_LENGTH = 64

    NAME_MAX_LENGTH = 100
    USERNAME_MIN_LENGTH = 2
    USERNAME_MAX_LENGTH = 30

    URL_MAX_LENGTH = 2048
    SLUG_MAX_LENGTH = 100

    RESERVED_USERNAMES = {
        "admin",
        "root",
        "api",
        "www",
        "mail",
        "ftp",
        "support",
        "help",
        "security",
        "privacy",
        "terms",
        "about",
        "contact",
        "blog",
        "news",
        "app",
        "application",
        "system",
        "test",
        "user",
        "guest",
        "demo",
        "null",
        "undefined",
        "none",
    }

    ALLOWED_URL_SCHEMES = {"http", "https"}
    BLOCKED_URL_DOMAINS = {
        "localhost",
        "127.0.0.1",
        "0.0.0.0",  # noqa: S104
        "::1",
        "[::1]",
    }
    SUSPICIOUS_URL_PATTERNS = ["javascript:", "data:", "vbscript:", "file:"]

validate = ValidationConfiguration()