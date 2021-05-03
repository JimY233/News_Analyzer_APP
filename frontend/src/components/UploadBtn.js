import React, { useState } from 'react';
import { Modal, Button, Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';
axios.defaults.withCredentials = true;

const UploadButton = ({cb}) => {
    const [visible, setVisible] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [fileList, setFileList] = useState([]);

    const showModal = () => {
        setVisible(true);
    };
    const handleUpload = async () => {
        setConfirmLoading(true);
        const formData = new FormData();
        fileList.forEach(file => {
            formData.append('file', file);
        });
        formData.append('file', fileList[0])
        setUploading(true);
        await axios.post('http://localhost:5000/api/multiupload', formData);
        setFileList([]);
        message.success('upload successfully');
        setUploading(false);
        setVisible(false);
        setConfirmLoading(false);
        cb();
    }

    const handleCancel = () => {
        console.log('cb')
        setVisible(false);
        
    };
    const props = {
        onRemove: file => {
            const index = fileList.indexOf(file);
            const newFileList = Array.from(fileList)
            newFileList.splice(index, 1)
            setFileList(newFileList);
        },
        beforeUpload: file => {
            setFileList([...fileList, file]);
            return false;
        },
        fileList,
    };
    return (
        <>
            <Button type="primary" onClick={showModal}>
                Upload Files
            </Button>
            <Modal
                title="Upload files"
                visible={visible}
                onOk={handleUpload}
                okText={uploading ? "Uploading" : "Upload"}
                cancelText="Cancel"
                confirmLoading={confirmLoading}
                onCancel={handleCancel}
            >
                <Upload {...props}>
                    <Button icon={<UploadOutlined />}>Select Files</Button>
                </Upload>
            </Modal>
        </>
    );
};

export default UploadButton;