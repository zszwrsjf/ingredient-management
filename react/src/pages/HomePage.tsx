import React from 'react';
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Paper,
  Stack,
} from '@mui/material';
import { Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import theme from '../themes/theme';
import Carousel from 'react-material-ui-carousel';

type ItemProps = {
  direction: 'row' | 'row-reverse';
  headText: string;
  subText: string;
  image: string;
  vertical?: boolean;
};

const Item: React.FunctionComponent<ItemProps> = (props) => {
  const cardHeight = 300;
  return (
    <Card sx={props.vertical ? {} : { height: cardHeight }}>
      <Box
        sx={
          props.vertical
            ? {}
            : { display: 'flex', flexDirection: props.direction }
        }
      >
        <CardContent
          sx={
            props.vertical
              ? {}
              : { width: '45%', flex: '1 0 auto', paddingX: 3 }
          }
        >
          <Typography component="div" variant="h4">
            {props.headText}
          </Typography>
          <Typography variant="h5" color="text.secondary" component="div">
            {props.subText}
          </Typography>
        </CardContent>
        <CardMedia
          component="img"
          image={props.image}
          alt={props.headText}
          sx={{ height: cardHeight }}
        />
      </Box>
    </Card>
  );
};

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="h4" gutterBottom>
            Welcome to
          </Typography>
          <Grid container spacing={0}>
            <Grid item xs={3} md={2}>
              <CardMedia
                src="/logo512.png"
                component="img"
                sx={{
                  height: '100%',
                  objectFit: 'scale-down',
                }}
              />
            </Grid>
            <Grid item xs={9} md={10}>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  flexWrap: 'wrap',
                  marginTop: 1.5,
                  marginLeft: 1,
                }}
              >
                <Typography
                  component="span"
                  variant="h3"
                  sx={{
                    paddingX: 2,
                    paddingY: 1,
                    color: 'white',
                    fontStyle: 'italic',
                    backgroundColor: theme.palette.primary.dark,
                  }}
                >
                  Health Up
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper variant="outlined" sx={{ padding: 3 }}>
            <Typography variant="h4" gutterBottom>
              About
            </Typography>
            <Typography variant="h5" sx={{ pt: 1 }}>
              <Typography
                variant="inherit"
                component="span"
                sx={{ fontStyle: 'italic' }}
              >
                Health Up
              </Typography>{' '}
              can let you eat{' '}
              <Typography variant="inherit" component="span" color="secondary">
                healthier
              </Typography>{' '}
              and be{' '}
              <Typography variant="inherit" component="span" color="secondary">
                happier
              </Typography>
              . And at the same time help you save money by reducing food waste!
            </Typography>
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Button
                variant="contained"
                color="secondary"
                onClick={() => navigate('/ingredients')}
                sx={{ paddingX: 3 }}
              >
                Get Started
              </Button>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={0} md={1} />
        <Grid item xs={12} md={10}>
          <Carousel sx={{ padding: 0.2 }} duration={500}>
            <Item
              direction="row"
              headText="Manage Your Inventory"
              subText="By pressing the plus button in the bottom right of screen, you can add new ingredient to your Health Up inventory."
              image="/images/instruction_01.png"
            />
            <Item
              direction="row-reverse"
              headText="Ingredient Expiration"
              subText="The progress bar under your ingredients' title indicates the time to
              expiration. The color goes from green to orange, then red. Don't hesitate to use them up before the expiration!"
              image="/images/instruction_02.png"
            />
            <Item
              direction="row"
              headText="Recipes by Ingredients"
              subText="Health Up allows you to find ways to use us your ingredients! Choose any or all of the ingredients. Then click on FIND RECIPES to get a list of optional recipes."
              image="/images/instruction_03.png"
            />
            <Item
              direction="row-reverse"
              headText="Refined Recipe Search"
              subText="Health Up can help you discover new dishes! In the Recipe Search page, try refining your search! Add or remove ingredients and set the filters as you desire."
              image="/images/instruction_04.png"
            />
          </Carousel>
        </Grid>
        <Grid item xs={0} md={1} />
      </Grid>
    </Box>
  );
};

export default HomePage;
