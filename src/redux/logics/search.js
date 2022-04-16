import axios from "axios";
import {API} from "../../config";
import {fetchSearchAction, resetSearchAction} from "../actions/search";

export const fetchSearch = (data) => dispatch => {
    return axios.get(API('search'),{
        params: data,
    }).then(res => {
        dispatch(fetchSearchAction({
            keyword: data.keyword,
            advanced: data.advanced,
            duration: res.duration || null,
            res: res.data, 
        }));
        return res.data;
    });
};

export const resetSearch = resetSearchAction;