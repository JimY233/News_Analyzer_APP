import React, { useState, useEffect } from 'react';
import { List } from 'antd';
import { LinkOutlined } from '@ant-design/icons';
import NewsView from './NewsView';
import axios from "axios";

axios.defaults.withCredentials = true

const NewsList = ({render}) => {
    const [data, setData] = useState({ newsnames: [] });
    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await axios.get(
                    'http://localhost:5000/api/getrecords'
                );
                setData({newsnames: res.data.newsnames.map(val => {
                    return {title: val[1], link: val[2]};
                    })
                });
            } catch (err) {
                console.log(err)
            }
        };
        fetchData();
    }, [render]);
    
    return (
        <List
            style={{maxHeight:'500px', overflowY:'auto'}}
            itemLayout="horizontal"
            dataSource={data.newsnames}
            renderItem={news => {
                return (
                    <List.Item>
                        <List.Item.Meta
                           title={<NewsView title={news.title}/>}
                            description={<a href={news.link} rel="noopener noreferrer" target="_blank"><LinkOutlined />{`Source Link`}</a>}
                        />
                    </List.Item>
            )}}
        />
    );
}
export default NewsList