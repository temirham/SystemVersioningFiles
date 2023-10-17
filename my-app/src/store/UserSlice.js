import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import axios from "axios";
import {ErrorStatus, IP4, LoadingStatus, SuccessStatus} from "./pref";

export const addUser1 = createAsyncThunk(
    'users/addUser',
    async (newUser) => {

        const requestOptions = {
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: newUser.username,
                password: newUser.password,
            })
        };
        console.log(newUser)
        const response = await axios.post(`${IP4}profiles_api/v1/token/get`, requestOptions);
        return response.data
    }
)

async function fetchJSON(url, options) {
    let response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`status code ${response.status}`);
    }
    return response.json();
}

export const addUser = createAsyncThunk(
    'users/addUser',
    async (newUser) => {

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: newUser.username,
                password: newUser.password,
            })
        };
        console.log(newUser)
        const response = await fetch(`${IP4}profiles_api/v1/signup`, requestOptions);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }
)



export const authUser = createAsyncThunk(
    'users/authUser',
    async (user) => {
        return await fetchJSON(
            `${IP4}profiles_api/v1/token/get`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
                body: JSON.stringify({
                    username: user.username,
                    password: user.password,
                })
            }
        )
    }
)
export const refreshUser = createAsyncThunk(
    'users/refreshUser',
    async () => {
        return await fetchJSON(
        `${IP4}profiles_api/v1/token/refresh`,
        {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
                body: JSON.stringify({
                    refresh: localStorage.getItem('refreshToken'),
                })
            }
        )
            // .then((data) => data.json())
    }
)

export const logoutUser = createAsyncThunk(
    'users/refreshUser',
    async () => {
        return await fetchJSON(
        `${IP4}profiles_api/v1/token/logout`,
        {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8',
                },
                body: JSON.stringify({
                    refresh: localStorage.getItem('refreshToken'),
                })
            }
        )
            // .then((data) => data.json())
    }
)


export const userSlice = createSlice({
    name: "userSlice",
    initialState: {
        username:"",
        password:"",
        accessToken:"",
        refreshToken:"",
        userStatus:"",
        userError:"",
        alertOpen:false,
        deleteDialogOpen:false
    },
    reducers: {
        exit: (state, action) => {
            state.userId=0;
            state.username = "";
            state.password="";
            state.accessToken="";
            localStorage.setItem('accessToken', '')
            state.refreshToken="";
            localStorage.setItem('refreshToken', '')
            state.userStatus=""
            state.userError=""
            state.alertOpen=false
            state.deleteDialogOpen=false
            localStorage.clear()
        },
        updateUsername: (state, action) => {
            state.username = action.payload;
        },
        updatePassword: (state, action) => {
            state.password = action.payload;
        },
        updateAccessToken: (state, action) => {
            state.accessToken = action.payload;
        },
        updateRefreshToken: (state, action) => {
            state.refreshToken = action.payload;
        },
        openAlert: (state, action) => {
            state.alertOpen = true;
        },
        closeAlert: (state, action) => {
            state.alertOpen = false;
        },
        openDeleteDialog: (state, action) => {
            state.deleteDialogOpen = true;
        },
        closeDeleteDialog: (state, action) => {
            state.deleteDialogOpen = false;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(addUser.pending, (state, action) => {
                state.userStatus=LoadingStatus
            })
            .addCase(addUser.fulfilled, (state, action) => {
                    state.userStatus = SuccessStatus
            })
            .addCase(addUser.rejected, (state, action) => {
                state.userStatus = ErrorStatus
                state.userError = action.error.message
            })
            .addCase(authUser.pending, (state, action) => {
                state.userStatus=LoadingStatus
            })
            .addCase(authUser.fulfilled, (state, action) => {
                state.accessToken=action.payload['access']
                state.refreshToken=action.payload['refresh']
                localStorage.setItem('accessToken', action.payload['access'])
                localStorage.setItem('refreshToken', action.payload['refresh'])
                state.userStatus = SuccessStatus
            })
            .addCase(authUser.rejected, (state, action) => {
                state.userStatus = ErrorStatus
                state.userError = action.error.message
            })
            .addCase(refreshUser.pending, (state, action) => {
                state.userStatus=LoadingStatus
            })
            .addCase(refreshUser.fulfilled, (state, action) => {
                state.accessToken=action.payload['access']
                localStorage.setItem('accessToken', action.payload['access'])
                state.userStatus = SuccessStatus
            })
            .addCase(refreshUser.rejected, (state, action) => {
                state.userStatus = ErrorStatus
                state.userError = action.error.message
            })
    }

})

export const {exit, updateUsername, updatePassword, updateAccessToken, updateRefreshToken,
    openAlert, closeAlert, openDeleteDialog, closeDeleteDialog,
}=userSlice.actions;
export default userSlice.reducer;