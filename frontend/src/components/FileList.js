import React, { useState, useEffect } from 'react';
import { List } from 'antd';
import { FileTextOutlined, FilePdfOutlined } from '@ant-design/icons'
import FileView from './FileView';
import axios from 'axios';

axios.defaults.withCredentials = true

const FileList = ({ render }) => {
    const [data, setData] = useState({ filenames: [] });
    useEffect(() => {
        const fetchData = async () => {
            const result = await axios('http://localhost:5000/api/getrecords');
            setData(result.data)
        };
        fetchData();
    }, [render]);
    
    return (
        <List
            style={{maxHeight:'500px', overflowY:'auto'}}
            itemLayout="horizontal"
            
            dataSource={data.filenames}
            renderItem={val => {
                const filename = val[0];
                const filetype = filename.split('.').pop().toLowerCase();
                return (
                    <List.Item>
                        <List.Item.Meta
                            avatar={filetype === 'pdf' ? <FilePdfOutlined style={{fontSize:'3em'}}/> : <FileTextOutlined style={{fontSize:'3em'}}/>}
                            title={<FileView filename={filename}/>}
                            // description="description"
                        />
                    </List.Item>
            )}}
        />
    );
}
export default FileList