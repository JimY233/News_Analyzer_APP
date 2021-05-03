import React, { useState } from 'react';
import { Card, Modal } from 'antd';
import axios from 'axios';
axios.defaults.withCredentials = true;

const FileView = (props) => {
    const [visible, setVisible] = useState(false);
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({ file: [] });
    
    const loadData = async () => {
        setVisible(true);
        setLoading(true);
        const res = await axios.get(`http://localhost:5000/api/show/${props.filename}`);
        setData({ file: {content:res.data.content, sentiment:res.data.sentiment} });
        setLoading(false);
    }

    return (
        <>
            <a onClick={loadData}>
                {props.filename}
            </a>
            <Modal
                title={props.filename}
                visible={visible}
                closable={true}
                onCancel={() => setVisible(false)}
                footer={[]}
                width='750px'
            >
                <Card loading={loading} bordered={false} style={{overflowY:'auto',height:'500px'}}>
                    <h1>Content</h1>
                    <p>{data.file.content}</p>
                    <h1>sentiment</h1>
                    <p>{JSON.stringify(data.file.sentiment)}</p>
                </Card>
            </Modal>
        </>
    );
}

export default FileView;