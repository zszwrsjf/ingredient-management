import axios, { AxiosError, AxiosRequestConfig } from 'axios';
import applyCaseMiddleware from 'axios-case-converter';

import { useContext } from 'react';
import AuthContext from '../context/authContext';
import { TAuthContext } from '../types/AuthContext';

export const useAxios = () => {
  const authCtx = useContext(AuthContext) as TAuthContext;

  const api = applyCaseMiddleware(
    axios.create({
      baseURL: process.env['REACT_APP_API_URL'],
      headers: {
        'Content-Type': 'application/json',
        ...(authCtx.isLoggedIn && {
          Authorization: `Bearer ${authCtx.token?.access}`,
        }),
      },
      // need a serializer to pass arrays as a parameter
      paramsSerializer: { indexes: null },
    })
  );

  const refresh = async () => {
    const res = await api.post('/token/refresh', {
      refresh: authCtx.token?.refresh,
    });
    return res.data?.access;
  };

  const refreshIntercept = api.interceptors.response.use(
    (res) => res,
    async (err: AxiosError) => {
      if (!err.config) {
        err.config = {};
      }
      const originalConfig: AxiosRequestConfig & { _retry?: boolean } =
        err.config;
      if (err.response?.status === 401 && !originalConfig?._retry) {
        originalConfig._retry = true;
        try {
          const token = await refresh();
          if (!token) {
            return Promise.reject(err);
          }
          authCtx.postRefresh(token);
          return api({
            ...originalConfig,
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
        } catch (_err) {
          return Promise.reject(_err);
        }
      }
      return Promise.reject(err);
    }
  );

  return {
    api,
    refreshIntercept,
    //...state,
    //dispatch,
  };
};
