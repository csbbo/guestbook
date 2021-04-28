import axios from 'axios'
import qs from 'qs'

const fetchData = (url = '', data = {}, method = 'GET') => {
    if (method === 'GET') {
        let param = qs.stringify(data)
        return new Promise(resolve => {
            axios.get(url+'?'+param).then((resp) => {
                resolve(resp.data)
            })
        })

    } else {
        return new Promise(resolve => {
            axios({
                method: method,
                url: url,
                data: data
            }).then((resp) => {
                resolve(resp.data)
            });
        })

    }
}


export const LoginAPI = data => fetchData('/api/login', data, 'POST')
export const RegistAPI = data => fetchData('/api/register', data, 'POST')
export const GetUser = () => fetchData('/api/user', {}, 'GET')

export const AddMessage = data => fetchData('/api/message/add', data, 'POST')
export const GetMessage = data => fetchData('/api/message/get', data, 'GET')
export const QueryMessage = data => fetchData('/api/message/query', data, 'GET')
export const DeleteMessage = data => fetchData('/api/message/delete', data, 'POST')
export const AddComment = data => fetchData('/api/comment/add', data, 'POST')
export const GetComment = data => fetchData('/api/comment/get', data, 'GET')
export const QueryComment = data => fetchData('/api/comment/query', data, 'GET')
