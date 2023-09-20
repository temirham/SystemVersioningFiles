import React from 'react';
import { List, ListItem, ListItemText } from '@mui/material';

function FileList({ files }) {
  return (
    <List>
      {files.map((file, index) => (
        <ListItem key={index}>
          <ListItemText primary={file.name} />
        </ListItem>
      ))}
    </List>
  );
}

export default FileList;
