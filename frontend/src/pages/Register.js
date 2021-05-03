import RegisterForm from '../components/RegisterForm';
import { useHistory } from "react-router-dom";
import { Card } from 'antd';
import './Register.css'

const Register = () => {
    let history = useHistory();
    const handleLogin = () => {
        history.push('/login');
    };
    return (
        <div className="container">
            <h1 className="title">News Analyzer</h1>
            <Card className="form">
                <RegisterForm/>
            </Card>
            <div>
                Already have an account? <a onClick={handleLogin}>Log in</a>
            </div>
        </div>
    )
}

export default Register