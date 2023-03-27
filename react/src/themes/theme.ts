import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#A0D700',
      light: '#B9F900',
      dark: '#91c200',
      contrastText: '#000',
    },
    secondary: {
      main: '#A9007A',
      light: '#E000A2',
      dark: '#7E005B',
      contrastText: '#fff',
    },
    info: {
      main: '#0455D6',
      light: '#146AF3',
      dark: '#043C96',
      contrastText: '#fff',
    },
    inactive: {
      main: '#d6d9dc',
      light: '#f1f2f3',
      dark: '#babfc4',
      contrastText: '#000',
    },
    highlight: {
      main: '#f6cf09',
      light: '#f8d83a',
      dark: '#ddba08',
      contrastText: '#000',
    },
    love: {
      main: '#e10505',
      light: '#fa1e1e',
      dark: '#c80404',
      contrastText: '#fff',
    },
  },
});

declare module '@mui/material/styles' {
  interface Palette {
    inactive: Palette['primary'];
    highlight: Palette['primary'];
    love: Palette['primary'];
  }

  // allow configuration using `createTheme`
  interface PaletteOptions {
    inactive?: PaletteOptions['primary'];
    highlight?: PaletteOptions['primary'];
    love?: PaletteOptions['primary'];
  }
}

// Update the Button's color prop options
declare module '@mui/material/Button' {
  interface ButtonPropsColorOverrides {
    inactive: true;
    highlight: true;
    love: true;
  }
}
declare module '@mui/material/IconButton' {
  interface IconButtonPropsColorOverrides {
    inactive: true;
    highlight: true;
    love: true;
  }
}

export default theme;
