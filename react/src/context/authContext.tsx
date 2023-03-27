import axios from 'axios';
import {
  createContext,
  FC,
  PropsWithChildren,
  useEffect,
  useState,
} from 'react';
import { useNavigate } from 'react-router-dom';
import { TAuthContext } from '../types/AuthContext';
import { Token } from '../types/Token';
import { User } from '../types/User';
import { decode } from '../util/jwt';

const AuthContext = createContext<TAuthContext | undefined>(undefined);

const getUserFromToken = (access_token: string) => {
  const decoded = decode(access_token);
  return {
    username: decoded.username,
    userId: decoded.user_id,
  };
};

export const AuthContextProvider: FC<PropsWithChildren> = (props) => {
  const [token, setToken] = useState<Token | undefined>();
  const [user, setUser] = useState<User | undefined>();
  const [isLoading, setIsLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      // local axios instance to avoid infinite call chains
      const client = axios.create({
        baseURL: process.env['REACT_APP_API_URL'],
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const storedTokenStr = localStorage.getItem('token');
      if (storedTokenStr) {
        const storedToken = JSON.parse(storedTokenStr) as Token;

        // validate the tokens
        try {
          await client.post('/token/verify', { token: storedToken.access });
          console.log('access token fetched from localStorage is valid');
          // nothing to do now; the token in localStorage is valid
        } catch (err) {
          console.log('access token fetched from localStorage is invalid');

          // try refreshing the access token
          try {
            const res = await client.post('/token/refresh', {
              refresh: storedToken.refresh,
            });
            localStorage.setItem(
              'token',
              JSON.stringify({
                ...storedToken,
                access: res.data.access,
              })
            );
          } catch (err) {
            console.log('refresh token fetched from localStorage is invalid');
            localStorage.removeItem('token');
          }
        }

        const updatedTokenStr = localStorage.getItem('token');
        if (updatedTokenStr) {
          const updatedToken = JSON.parse(updatedTokenStr) as Token;
          setToken(updatedToken);
          setUser(getUserFromToken(updatedToken.access));
        }
      }
      setIsLoading(false);
    })();
  }, []);

  const loginHandler = (token: Token) => {
    localStorage.setItem('token', JSON.stringify(token));
    setToken(token);
    setUser(getUserFromToken(token.access));
  };

  const logoutHandler = () => {
    localStorage.removeItem('token');
    setToken(undefined);
    setUser(undefined);
    navigate('/auth/login', { replace: true });
  };

  const refreshTokenHandler = (newAccessToken: string) => {
    if (!token) {
      console.log('refresh should be called after login');
      return;
    }
    setToken((prev) => {
      if (!prev) {
        console.log('Unexpectedly called refresh token before having a token');
        return undefined;
      }
      const newToken = {
        ...prev,
        access: newAccessToken,
      };
      localStorage.setItem('token', JSON.stringify(newToken));
      return newToken;
    });
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isLoading,
        postLogin: loginHandler,
        logout: logoutHandler,
        postRefresh: refreshTokenHandler,
        isLoggedIn: !!token?.access,
      }}
    >
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
