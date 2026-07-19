import http from './http'

export const fetchHomeRecommend = () => http.get('/videos/home-recommend/')
export const fetchVideos = (params) => http.get('/videos/', { params })
export const fetchVideoDetail = (id) => http.get(`/videos/${id}/`)
export const playAuth = (id) => http.post(`/videos/${id}/play-auth/`)
export const fetchDanmaku = (id) => http.get(`/videos/${id}/danmaku/`)
export const submitDanmaku = (id, data) => http.post(`/videos/${id}/danmaku/`, data)
export const toggleFavorite = (id) => http.post(`/videos/${id}/favorite/`)
export const cancelFavorite = (id) => http.delete(`/videos/${id}/favorite/`)
export const checkMembership = () => http.get('/membership/check/')
export const fetchMembershipPlans = () => http.get('/membership-plans/')
