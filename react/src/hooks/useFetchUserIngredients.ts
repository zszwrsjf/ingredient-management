import type { UserIngredient } from '../types/UserIngredient';
import { useCallback, useState } from 'react';
import { useAxios } from './useAxios';

export const useFetchUserIngredients = () => {
  const [userIngredients, setUserIngredients] = useState<UserIngredient[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { api } = useAxios();

  const onChangeUserIngredients = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await api.get('/user/ingredients');
      const userIngredients = res.data;

      setUserIngredients(userIngredients);
    } catch (err) {
      console.log(err);
    }
    setIsLoading(false);
  }, []);

  return { userIngredients, onChangeUserIngredients, isLoading };
};
