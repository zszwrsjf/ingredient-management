import { Ingredient } from './Ingredient';

export type RecipeIngredient = {
  id: number;
  ingredient: Ingredient;
  recipe?: number; // maybe remove
  weight: number;
  quantityValue: number;
  quantityScale: number;
};
