import { useCallback, useState } from 'react';
import type { Recipe } from '../types/Recipe';
import { useAxios } from './useAxios';
import { Ingredient } from '../types/Ingredient';

export const useFetchRecipes = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { api } = useAxios();

  const onChangeRecipes = useCallback(
    async (
      ingredients?: Ingredient['id'][],
      mode?: 'any' | 'exact',
      strict?: boolean
    ) => {
      setIsLoading(true);
      try {
        const res = await api.get(`/recipes/search`, {
          params: {
            ingredient: ingredients,
            mode: mode || 'any',
            strict: strict || false,
          },
        });
        const recipes = res.data;

        setRecipes(recipes);
      } catch (err) {
        console.log(err);
      }
      setIsLoading(false);
    },
    []
  );

  return { recipes, onChangeRecipes, isLoading };
};
