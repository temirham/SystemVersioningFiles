import React, { useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Input, Paper, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';

import { addFile, loadFiles, uploadFile} from '/Users/temirhanmamaev/Documents/test_front/my-app/src/store/fileSlice.js';
import axios from 'axios';
import {useDispatch, useSelector} from "react-redux";

function countFileRepetitions(files, fileName) {
  let maxVersion = 0;

  files.forEach((file) => {
    if (file.name === fileName && file.version > maxVersion) {
      maxVersion = file.version;
    }
  });

  return maxVersion;
}




function FileUploader() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDialogOpen, setDialogOpen] = useState(false);
  const {files} = useSelector((state) => state.files); 
  const dispatch = useDispatch();
//   const {userId} = useSelector((state) => state.userId);
  

  const openDialog = () => {
    setDialogOpen(true);
  };

  const closeDialog = () => {
    setDialogOpen(false);
    setSelectedFile(null);
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (selectedFile) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        dispatch(uploadFile(formData)).then(() => 
          {dispatch(loadFiles())}
        );
        closeDialog()
      }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setSelectedFile(file);
  };

  return (
    <div>
      <Button startIcon={<CloudUploadIcon />} variant="contained" color="primary" onClick={openDialog}>
        Выгрузить файл
      </Button>
      <Dialog open={isDialogOpen} onClose={closeDialog} maxWidth="md">
        <DialogTitle>Select a File</DialogTitle>
        <DialogContent>
          <Paper
            elevation={3}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            style={{
              padding: '40px',
              textAlign: 'center',
              cursor: 'pointer',
              minWidth: '500px',
              minHeight: '300px' 
            }}
          >
            {selectedFile ? (
              <div>
                <InsertDriveFileIcon
                  style={{
                    fontSize: '72px', 
                    color: 'gray', 
                    marginBottom: '20px', 
                  }}
                />
                <Typography variant="h6">Выберите файл:</Typography>
                <Typography variant="subtitle1">{selectedFile.name}</Typography>
              </div>
            ) : (
              <div>
                <Typography variant="h6">Перетащите файл сюда</Typography>
                <Typography variant="h6">или</Typography>
                <Input type="file" onChange={handleFileChange} style={{ display: 'none' }} id="file-input" />
                <label htmlFor="file-input">
                  <Button
                    variant="contained"
                    color="primary"
                    component="span"
                    startIcon={<CloudUploadIcon />}
                    
                  >
                    Выбрать из проводника
                  </Button>
                </label>
              </div>
            )}
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeDialog} color="primary">
            Close
          </Button>
          {selectedFile && (
            <Button onClick={handleUpload} color="primary">
              Upload
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default FileUploader;
