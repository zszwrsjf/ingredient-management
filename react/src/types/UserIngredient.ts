import { Ingredient } from './Ingredient';

export type UserIngredient = {
  id: number;
  quantityValue: number;
  consumed: boolean;
  storage: number;
  createdDate: string;
  expirationDate: string;
  happiness: number;
  user: number;
  ingredient: Ingredient;
  quantityScale: number;
};
