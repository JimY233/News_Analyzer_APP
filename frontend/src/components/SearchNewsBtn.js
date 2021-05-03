import React, { useState } from 'react';
import { Modal, Button, List, Input, Spin } from 'antd';
import { LinkOutlined } from '@ant-design/icons';
import axios from 'axios';
axios.defaults.withCredentials = true;
const { Search } = Input;

const SearchNewBtn = ({ cb }) => {
    const [visible, setVisible] = useState(false);
    const [loading, setLoading] = useState(false);
    const [showResult, setShowResult] = useState(false);
    const [data, setData] = useState({ news: [] })
    const [spinning, setSpinning] = useState(false);

    const showModal = () => {
        setVisible(true);
    };
    const handleSearch = async keyword => {
        setShowResult(false);
        setLoading(true);
        const fetchData = async () => {
            const res = await axios.post(
                'http://localhost:5000/api/ingest',
                {num: 10, keyword: keyword}
            );
            console.log('search result:',res.data.newsnames);
            console.log('before setData:', data)
            setData({news: res.data.newsnames.map(val => {
                return {title: val[2], link: val[3]};
                })
            });
            console.log('before setData:', data)
        };
        fetchData();
        setLoading(false);
        setShowResult(true);
    }

    const handleCancel = () => {
        setVisible(false);
        setShowResult(false)
        cb();
    };

    const saveNews = async (title) => {
        setSpinning(true);
        console.log('trying to save news with title', title)
        const res = await axios.get(`http://localhost:5000/api/save_news/${title}`);
        console.log(res);
        setSpinning(false);
    }
    
    return (
        <>
            <Button type="primary" onClick={showModal}>
                Search News
            </Button>
            <Modal
                title="Search News"
                visible={visible}
                closable={true}
                onCancel={handleCancel}
                destroyOnClose={true}
                footer={[]}
            >
                <Search 
                    placeholder="search news"
                    enterButton="Search"
                    size="large"
                    onSearch={handleSearch}
                    loading={loading}
                />
                <div>
                    { showResult 
                    ? <Spin spinning={spinning}>
                        <List 
                        style={{height:'400px', overflowY:'auto'}}
                        itemLayout="horizontal"
                        dataSource={data.news}
                        locale={{emptyText:'searching...'}}
                        renderItem={news => {
                            return (
                                <List.Item>
                                    <List.Item.Meta
                                        title={<p>{news.title}</p>}
                                        description={<a href={news.link} rel="noopener noreferrer" target="_blank"><LinkOutlined />{`Source Link`}</a>}
                                    />
                                    <Button onClick={() => saveNews(news.title)}>
                                        Save
                                    </Button>
                                </List.Item>
                        )}}
                    /></Spin>
                    : <></>}
                </div>
            </Modal>
        </>
    );
};

export default SearchNewBtn;