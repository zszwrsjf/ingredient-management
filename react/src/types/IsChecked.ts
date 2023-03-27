import { UserIngredient } from './UserIngredient';

export type IsChecked = {
  [key: UserIngredient['id']]: boolean;
};
