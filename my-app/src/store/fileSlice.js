import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { IP4, LoadingStatus, SuccessStatus } from "./pref";


async function fetchJSON(url, options) {
    let response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`status code ${response.status}`);
    }
    return response.json();
}

export const loadFiles = () => async (dispatch) => {
    try {
      const response = await axios.get(`https://650a3278f6553137159c7e12.mockapi.io/uploadFile`); // Загрузите файлы с сервера
      dispatch(setFile(response.data)); // Обновите состояние с файлами
    } catch (error) {
      // Обработка ошибок
    }
  };

// Замените Note на FileVersion
export const getUserFile = createAsyncThunk(
  'file/getUserFile',
  //async (userId) => {
  async () => {
    // const requestOptions = {
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
    //   },
    // };
    // const response = await axios.get(`${IP4}file/${userId}`, requestOptions);
    const response = await axios.get(`https://650a3278f6553137159c7e12.mockapi.io/uploadFile`);
    return response.data.data
  }
);

// Замените Note на FileVersion
export const addFile = createAsyncThunk(
  'file/addFile',
  async (file) => {
    return await fetchJSON(
      `${IP4}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        body: JSON.stringify({
          user: file.user,
          name: file.name,
          version: file.version,
          content: file.content,
        })
      }
    );
  }
);

export const uploadFile = createAsyncThunk(
    'file/uploadFile',
    async ({ file, userId }) => {
      const formData = new FormData();
      formData.append('user', userId);
      formData.append('file', file);
  
      const requestOptions = {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
      };
  
      const response = await axios.post(`${IP4}upload_file`, formData, requestOptions);
      return response.data.data;
    }
  );

// Замените Note на FileVersion
export const editFile = createAsyncThunk(
  'file/editFile',
  async (file) => {
    return await fetchJSON(
      `${IP4}file/edit`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        body: JSON.stringify({
          user: file.user,
          newFileName: file.newFileName,
          version: file.version,
          content: file.content,
          name: file.name,
          date: file.date,
        })
      }
    );
  }
);

// Замените Note на FileVersion
export const deleteFile = createAsyncThunk(
  'fileVersions/deleteFileVersion',
  async (file) => {
    return await fetchJSON(
      `${IP4}fileVersions/delete`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        body: JSON.stringify({
          user: file.user,
          name: file.name,
        })
      }
    );
  }
);

export const fileSlice = createSlice({
  name: "fileSlice",
  initialState: {
    files: [],
    fileStatus: '',
    currentFile: {
      fileName: '',
      version: 0,
      path: '',
      date: '',
    },
    deletingFile: {
      fileName: '',
      version: 0,
      path: '',
      date: '',
    },
    fileName: '',
  },
  reducers: {
    clearFile: (state, action) => {
      state.files = [];
      state.fileStatus = '';
      state.currentFile = {
        fileName: '',
        version: 0,
        path: '',
        date: '',
      };
      state.deletingFile = {
        fileName: '',
        version: 0,
        content: '',
        date: '',
      };
      state.fileName = '';
      localStorage.clear();
    },
    setFile: (state, action) => {
      state.files = action.payload;
    },
    setCurrentFile: (state, action) => {
      state.currentFile = action.payload;
    },
    setDeletingFile: (state, action) => {
      state.deletingFileVersion = action.payload;
    },
    setFileName: (state, action) => {
      state.fileName = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getUserFile.pending, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(getUserFile.fulfilled, (state, action) => {
        state.fileStatus = SuccessStatus;
        state.files = action.payload;
        state.currentFile = state.files[0];
        state.fileName = state.files[0].fileName;
        localStorage.setItem('file', JSON.stringify(state.files));
      })
      .addCase(getUserFile.rejected, (state, action) => {
        state.fileStatus = LoadingStatus;
        state.files = JSON.parse(localStorage.getItem('file'));
      })
      .addCase(addFile.pending, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(addFile.fulfilled, (state, action) => {
        state.fileStatus = SuccessStatus;
      })
      .addCase(addFile.rejected, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(editFile.pending, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(editFile.fulfilled, (state, action) => {
        state.fileStatus = SuccessStatus;
      })
      .addCase(editFile.rejected, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(deleteFile.pending, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(deleteFile.fulfilled, (state, action) => {
        state.fileStatus = SuccessStatus;
      })
      .addCase(deleteFile.rejected, (state, action) => {
        state.fileStatus = LoadingStatus;
      });
  }
});

export const {
  clearFile,
  setFile,
  setCurrentFile,
  setDeletingFile,
  setOldFileName,
} = fileSlice.actions;

export default fileSlice.reducer;
