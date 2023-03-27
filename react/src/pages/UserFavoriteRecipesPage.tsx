import * as React from 'react';
import { Box, Stack, Typography, Grid, Divider, Button } from '@mui/material';
import AuthContext from '../context/authContext';
import { TAuthContext } from '../types/AuthContext';
import { UserBasicInfo } from '../components/UserBasicInfo';
import { useFetchUserInfo } from '../hooks/useFetchUserInfo';
import { iso_to_string } from '../util/misc';
import RecipeCard from '../components/RecipeCard';
import { UserHistoryRecipeItem } from '../types/UserInfo';
import RecipeItem from '../components/RecipeItem';
import LoadingOverlay from '../components/LoadingOverlay';

const UserFavoriteRecipesPage: React.FunctionComponent = () => {
  const authCtx = React.useContext(AuthContext) as TAuthContext;
  const { userInfo, onChangeUserInfo, isLoading } = useFetchUserInfo();

  React.useEffect(() => {
    onChangeUserInfo();
  }, []);

  console.log(authCtx.user);

  return (
    <React.Fragment>
      <LoadingOverlay isLoading={isLoading} />
      <Box className="user-dashboard-container">
        <Stack direction="column" spacing={2}>
          <Box className="user-dashboard-info" marginBottom={3}>
            <UserBasicInfo title="Favorite Recipes" user={authCtx.user} />
          </Box>
          <Divider textAlign="left">
            <Typography variant="h5">Favorites</Typography>
          </Divider>
          <Stack
            direction="row"
            sx={{
              flexWrap: 'wrap',
              columnGap: 3,
              rowGap: 3,
            }}
          >
            <Grid container spacing={3}>
              {userInfo?.recipeFavorites.map((fav_recipe) => {
                return (
                  <Grid item key={fav_recipe.id} xs={12} md={3}>
                    <RecipeCard
                      recipe={fav_recipe.recipe}
                      mediaHeight={200}
                      subText={`Added: ${iso_to_string(fav_recipe.addedDate)}`}
                    ></RecipeCard>
                  </Grid>
                );
              })}
            </Grid>
          </Stack>
        </Stack>
      </Box>
    </React.Fragment>
  );
};

export default UserFavoriteRecipesPage;
