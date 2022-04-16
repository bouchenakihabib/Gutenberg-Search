export const IS_DEV = !process.env.NODE_ENV || process.env.NODE_ENV === 'development';

export const URL = 'http://127.0.0.1:8000';


export const API = (model = undefined, id = undefined) => {
    if (model && id) {
        return `${URL}/api/${model}/${id}/`;
    }
    if (model) {
        return `${URL}/api/${model}/`;
    }
    return `${URL}/api/`;
};

export const TIMEOUT = 120 * 1000; // in ms (2 minutes)

export const TITLE = (section) => `Gutenberg-Search - ${section}`;

export const BASE_NAME = IS_DEV ? '' : '/Gutenberg_Search';