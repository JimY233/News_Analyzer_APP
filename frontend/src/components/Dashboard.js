import React, { useState } from 'react';
import { Card, Row, Col } from 'antd';
import UploadBtn from './UploadBtn';
import SearchNewBtn from "./SearchNewsBtn";
import FileList from './FileList';
import NewsList from './NewsList';

const Dashboard = () => {
    const [renderFileList, setRenderFileList] = useState([]);
    const [renderNewsList, setRenderNewsList] = useState([]);
    const renderFileListCallback = () => {
        setRenderFileList([...renderFileList]);
    }
    const renderNewsListCallback = () => {
        setRenderNewsList([...renderNewsList]);
    }
    return (
        <div className="site-card-wrapper" >
            <Row gutter={8}>
                <Col span={12}>
                    <Card title="Files" bordered={true}
                    style={{width:'450px'}}>
                        <FileList render={renderFileList}/>
                        <div style={{textAlign:'center'}}>
                            <UploadBtn cb={renderFileListCallback}/>
                        </div>
                    </Card>
                </Col>
                <Col span={12}>
                    <Card title="News" bordered={true} 
                    style={{width:'450px'}}>
                        <NewsList render={renderNewsList}/>
                        <div style={{textAlign:'center'}}>
                            <SearchNewBtn cb={renderNewsListCallback}/>
                        </div>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}

export default Dashboard