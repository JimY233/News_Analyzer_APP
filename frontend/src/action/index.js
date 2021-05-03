import axios from 'axios';
axios.defaults.withCredentials = true;

export const fetchUser = () => async dispatch => {
    const res = await axios.get('http://localhost:5000/api/current_user');
    console.log('res.data is ', res.data)
    dispatch({ type: 'fetch_user', payload: res.data.user_id });
};

export const login = (values, history, message) => async dispatch => {
    const res = await axios.post('http://localhost:5000/api/login', values, {'Content-Type': 'application/json'})
    if (res.data.status === 'success') {
        message.success('login success', 1)
        history.push('/');
    } else {
        message.error(res.data.message)
    }
    console.log('after login, res.data is ', res.data)
    dispatch({ type: 'fetch_user', payload: res.data.user });
}