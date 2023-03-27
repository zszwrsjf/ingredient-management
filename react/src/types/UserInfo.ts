import { Recipe } from './Recipe';

export type UserHistoryRecipeItem = {
  id: number;
  user: number;
  recipe: Recipe;
  accessDate: string;
  cooked: boolean;
};

export type UserFavoriteRecipeItem = {
  id: number;
  user: number;
  recipe: Recipe;
  addedDate: string;
};

export type UserInfo = {
  user: number;
  allCooked: number;
  allLiked: number;
  allIngredients: number;
  recipeHistory: UserHistoryRecipeItem[];
  recipeFavorites: UserFavoriteRecipeItem[];
};
