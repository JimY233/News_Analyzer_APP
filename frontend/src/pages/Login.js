import LoginForm from '../components/LoginForm';
import { useHistory } from "react-router-dom";
import { Card } from 'antd';
import './Login.css'

const Register = () => {
    let history = useHistory();
    const handleSignup = () => {
        history.push('/signup');
    };
    return (
        <div className="container">
            <div className="title">News Analyzer</div>
            <Card className="form">
                <LoginForm/>
            </Card>
            <div>
                Don't have an account? <a onClick={handleSignup}>Sign up</a>
            </div>
        </div>
    )
}

export default Register