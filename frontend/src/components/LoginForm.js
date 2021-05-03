import React from 'react';
import { Form, Input, Button, message } from 'antd';
import { withRouter } from "react-router-dom";
import 'antd/dist/antd.css';
import axios from 'axios';
import { connect } from 'react-redux';
import * as actions from '../action/index'
axios.defaults.withCredentials = true

const formItemLayout = {
    labelCol: {
        xs: {
            span: 24,
        },
        sm: {
            span: 8,
        },
    },
    wrapperCol: {
        xs: {
            span: 24,
        },
        sm: {
            span: 16,
        },
    },
};
const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24,
            offset: 0,
        },
        sm: {
            span: 16,
            offset: 8,
        },
    },
};

const LoginForm = ({login, history}) => {
    const [form] = Form.useForm();
    const onFinish = (values) => login(values, history, message);

    return (
        <Form
            {...formItemLayout}
            form={form}
            name="login"
            onFinish={onFinish}
        >
            <Form.Item
                name="username"
                label="Username"
                rules={[
                    {
                        required: true,
                        message: 'Please input your username!',
                        whitespace: true,
                    },
                ]}
            >
                <Input placeholder="username"/>
            </Form.Item>

            <Form.Item
                name="password"
                label="Password"
                rules={[
                    {
                        required: true,
                        message: 'Please input your password!',
                    },
                ]}
            >
                <Input.Password />
            </Form.Item>

            <Form.Item {...tailFormItemLayout}>
                <Button type="primary" htmlType="submit">
                    Log In
                </Button>
            </Form.Item>
        </Form>
    );
};

function mapStateToProps({auth}) {
    return { auth };
}

export default connect(mapStateToProps, actions)(withRouter(LoginForm));
