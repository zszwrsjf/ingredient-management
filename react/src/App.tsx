import { ThemeProvider } from '@mui/material';
import theme from './themes/theme';
import UserDashboardPage from './pages/UserDashboardPage';
import { Route, Routes } from 'react-router-dom';
import PrivateRoute from './components/PrivateRoute';
import Layout from './components/layout/Layout';
import UserFavoriteRecipesPage from './pages/UserFavoriteRecipesPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import MyIngredientsPage from './pages/MyIngredientsPage';
import SearchRecipesPage from './pages/SearchRecipesPage';
import HomePage from './pages/HomePage';

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <Layout>
        <Routes>
          {/* public routes */}
          <Route index element={<HomePage />} />
          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/auth/signup" element={<SignupPage />} />
          <Route path="/recipes" element={<SearchRecipesPage />} />
          {/* private routes */}
          <Route element={<PrivateRoute />}>
            <Route
              path="/ingredients"
              element={<MyIngredientsPage allowAddIngredient />}
            />
            <Route path="/user" element={<UserDashboardPage />} />
            <Route
              path="/user/favorites"
              element={<UserFavoriteRecipesPage />}
            />
          </Route>
        </Routes>
      </Layout>
    </ThemeProvider>
  );
};

export default App;
