import {useEffect} from "react";
import axios from "axios"
import {useDispatch} from "react-redux";
import { setFile } from "../store/fileSlice";


export async function GetFiles() {
    const dispatch = useDispatch()
    async function fetchData() {
        const response = await axios.get('https://650a3278f6553137159c7e12.mockapi.io/uploadFile') // получение данных с API
        dispatch(setFile(response.data))
    }
    useEffect(() => {
        fetchData()
    }, [])
}

