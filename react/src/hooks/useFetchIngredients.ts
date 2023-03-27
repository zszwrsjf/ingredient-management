import { useCallback, useState } from 'react';
import { useAxios } from './useAxios';
import { Ingredient } from '../types/Ingredient';

export const useFetchIngredients = () => {
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { api } = useAxios();

  const onChangeIngredients = useCallback(async (ids: number[]) => {
    setIsLoading(true);
    try {
      const res = await api.get(`/ingredients`, {
        params: {
          ingredient: ids,
        },
      });
      setIngredients(res.data);
    } catch (err) {
      console.log(err);
    }
    setIsLoading(false);
  }, []);

  return { ingredients, onChangeIngredients, isLoading };
};
