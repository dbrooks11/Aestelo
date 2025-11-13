import Cookies from 'js-cookie'


export const csrfAccessToken = (): string | undefined =>{
    return Cookies.get('csrf_access_token')
}

export const csrfRefreshToken = (): string | undefined =>{
    return Cookies.get('csrf_refresh_token')
}