import { Token } from './Token';
import { User } from './User';

export type TAuthContext = {
  token?: Token;
  user?: User;
  isLoggedIn: boolean;
  isLoading: boolean;
  postLogin: (token: Token) => void;
  logout: () => void;
  postRefresh: (newAccessToken: string) => void;
};
