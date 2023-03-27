import { RecipeIngredient } from './RecipeIngredient';
import { Nutrition } from './Nutrition';
import { Tag } from './Tag';

export type Recipe = {
  id: number;
  title: string;
  recipeUrl: string;
  imageUrl: string;
  cookMinute: number;
  numServings: number;
  language: string;
  numIngredients: number;
  userCooked?: boolean;
  allCooked?: number;
  userFavorite?: boolean;
  allFavorite?: number;
  nutrition?: Nutrition;
  tags?: Tag[];
  ingredients?: RecipeIngredient[];
};
