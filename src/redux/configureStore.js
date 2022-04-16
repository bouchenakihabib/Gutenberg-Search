import {createStore, applyMiddleware} from 'redux';
import logger from 'redux-logger';
import rootReducer from './rootReducer';
import thunk from 'redux-thunk';
import promise from 'redux-promise-middleware';
import storage from 'redux-persist/lib/storage';
import {persistStore, persistReducer} from 'redux-persist';
import packageInfo from "../../package.json";
import {IS_DEV} from "../config";


const persistConfig = {
    key: 'root',
    keyPrefix: packageInfo.name,
    storage: storage,
};

const middlewares = [thunk, promise];

if (IS_DEV) {
    middlewares.push(logger);
}

const persistedReducer = persistReducer(persistConfig, rootReducer);

export default () => {
    let store = createStore(persistedReducer, applyMiddleware(...middlewares));
    let persistor = persistStore(store);
    return {store, persistor};
};