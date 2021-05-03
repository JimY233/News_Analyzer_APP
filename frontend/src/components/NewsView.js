import React, { useState } from 'react';
import { Card, Modal } from 'antd';
import axios from 'axios';
axios.defaults.withCredentials = true;

const NewsView = (props) => {
    const [visible, setVisible] = useState(false);
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({ news: [] });
    
    const loadData = async () => {
        setVisible(true);
        setLoading(true);
        const res = await axios.get(`http://localhost:5000/api/shownews/${props.title}`);
        setData({ news: {content:res.data.content, sentiment:res.data.sentiment} });
        console.log(data)
        setLoading(false);
    }

    return (
        <>
            <a onClick={loadData}>
                {props.title}
            </a>
            <Modal
                title={props.title}
                visible={visible}
                closable={true}
                onCancel={() => setVisible(false)}
                footer={[]}
                width='750px'
            >
                <Card loading={loading} bordered={false} style={{overflowY:'auto',height:'500px'}}>
                    <h1>Content</h1>
                    <p>{data.news.content}</p>
                    <h1>sentiment</h1>
                    <p>{JSON.stringify(data.news.sentiment)}</p>
                </Card>
            </Modal>
        </>
    );
}

export default NewsView;