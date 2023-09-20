import { configureStore } from "@reduxjs/toolkit";
import userReducer from './UserSlice';
import fileReducer from './fileSlice'; // Импортируйте редюсер для файлов

export default configureStore({
  reducer: {
    userId:userReducer,
    username:userReducer,
    password:userReducer,
    accessToken:userReducer,
    refreshToken:userReducer,
    userStatus:userReducer,
    userError:userReducer,
    alertOpen:userReducer,
    deleteDialogOpen:userReducer,

    files:fileReducer,
    fileStatus:fileReducer,
    currentFiles:fileReducer,
    fileName:fileReducer,
    //     deletingNote:noteReducer,
    //     oldTitle:noteReducer, // Добавьте редюсер для файлов
    // Добавьте другие редюсеры для файлов при необходимости
  }
});
