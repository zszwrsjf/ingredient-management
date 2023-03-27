export type Ingredient = {
  id: number;
  name: string;
  infoUrl: string;
  imageUrl: string;
  category: string;
  pantryDays: number | null;
  refrigeratorDays: number | null;
  freezerDays: number | null;
  inStorage: boolean;
};
