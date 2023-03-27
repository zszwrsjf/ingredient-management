import { useCallback, useState } from 'react';
import { UserInfo } from '../types/UserInfo';
import { useAxios } from './useAxios';

export const useFetchUserInfo = () => {
  const [userInfo, setUserInfo] = useState<UserInfo>();
  const [isLoading, setisLoading] = useState(false);
  const { api } = useAxios();

  const onChangeUserInfo = useCallback(async () => {
    setisLoading(true);
    try {
      const [res1, res2, res3] = await Promise.all([
        api.get(`/user/stats`),
        api.get(`/user/recipes`),
        api.get(`/user/favorite`),
      ]);
      setUserInfo({
        ...res1.data,
        recipeHistory: res2.data,
        recipeFavorites: res3.data,
      });
    } catch (err) {
      console.log(err);
    }
    setisLoading(false);
  }, []);

  return { userInfo, onChangeUserInfo, isLoading };
};
