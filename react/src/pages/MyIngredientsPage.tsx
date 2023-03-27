import * as React from 'react';

import theme from '../themes/theme';
import { IsChecked } from '../types/IsChecked';
import { IngredientList } from '../components/IngredientList';
import IngredientForm from '../components/form/ingredient/IngredientForm';
import LoadingOverlay from '../components/LoadingOverlay';
import { useFetchUserIngredients } from '../hooks/useFetchUserIngredients';

import { useNavigate } from 'react-router-dom';
import Modal from 'react-modal';

import {
  alpha,
  Box,
  Button,
  Container,
  Stack,
  Typography,
} from '@mui/material';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';
import { grey } from '@mui/material/colors';

type MyIngredientsPageProps = { allowAddIngredient?: boolean };

const MyIngredientsPage: React.FunctionComponent<MyIngredientsPageProps> = (
  props
) => {
  const { userIngredients, onChangeUserIngredients, isLoading } =
    useFetchUserIngredients();

  React.useEffect(() => {
    onChangeUserIngredients();
  }, []);

  // Create a state dictionary whose form is ingredientId: isChecked
  const isChecked: IsChecked = [];
  for (const userIngredient of userIngredients) {
    isChecked[userIngredient.ingredient.id] = false;
  }

  const [isCheckedState, setIsCheckedState] =
    React.useState<IsChecked>(isChecked);

  // checkedCount stores how many checkboxes are filled
  // It is used to control whether to display Find Recipes button
  const [checkedCount, setCheckedCount] = React.useState(0);

  // This value determines the size of Find Recipes button
  const findRecipesButtonMagnificationRate = 1.5;
  const addIngredientButtonMagnificationRate = 1.5;

  const navigate = useNavigate();

  // handleChange is triggered when a checkbox is clicked
  const handleChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setIsCheckedState((prevIsCheckedState) => {
        return {
          ...prevIsCheckedState,
          [event.target.name]: event.target.checked,
        };
      });
      if (event.target.checked) {
        setCheckedCount((prev) => prev + 1);
      } else {
        setCheckedCount((prev) => prev - 1);
      }
    },
    []
  );

  // Ingredient form related stuff below
  const [modalIsOpen, setModalIsOpen] = React.useState(false);
  const toggleModal = React.useCallback(() => {
    setModalIsOpen((prev) => !prev);
  }, []);

  // onSubmit includes reloading userIngredients
  const onSubmit = React.useCallback(() => {
    toggleModal();
    onChangeUserIngredients();
  }, []);

  const onIngredientAction = React.useCallback(() => {
    onChangeUserIngredients();
  }, []);

  const setCheckAllAction = (mode: boolean) => {
    for (const userIngredient of userIngredients) {
      isChecked[userIngredient.ingredient.id] = mode;
    }
    setIsCheckedState(isChecked);
    setCheckedCount(mode ? userIngredients.length : 0);
  };

  const modalStyle: Modal.Styles = {
    overlay: {
      backgroundColor: alpha(grey[500], 0.5),
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 1, // disallow the btns in the layer below
    },
    content: {
      position: 'relative',
      inset: '0',
      width: 'fit-content',
      height: 'fit-content',
      margin: '0 auto',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      borderRadius: '10px',
    },
  };

  const FindRecipesButton = () => {
    if (checkedCount > 0) {
      return (
        <Fab
          variant="extended"
          color="primary"
          aria-label="find recipes"
          onClick={() => {
            navigate('/recipes', { state: JSON.stringify(isCheckedState) });
          }}
          sx={{
            position: 'fixed',
            bottom: theme.spacing(6),
            left: theme.spacing(6),
            // default size * magnification rate
            width: 126.07 * findRecipesButtonMagnificationRate,
            height: 48 * findRecipesButtonMagnificationRate,
            borderRadius: 24 * findRecipesButtonMagnificationRate,
            fontSize: `${0.8 * findRecipesButtonMagnificationRate}em`,
          }}
        >
          Find Recipes
        </Fab>
      );
    } else {
      return <></>;
    }
  };

  return (
    <React.Fragment>
      <LoadingOverlay isLoading={isLoading} />
      <Stack direction="row" spacing={2} sx={{ margin: 3 }}>
        <Button
          variant="contained"
          disableElevation
          onClick={() => setCheckAllAction(true)}
        >
          Select All
        </Button>
        <Button
          variant="outlined"
          color="secondary"
          disabled={checkedCount <= 0}
          onClick={() => setCheckAllAction(false)}
        >
          Deselect All
        </Button>
      </Stack>
      <IngredientList
        userIngredients={userIngredients}
        isCheckedState={isCheckedState}
        handleChange={handleChange}
        onAction={onIngredientAction}
      />
      <FindRecipesButton />
      {props.allowAddIngredient && (
        <Fab
          color="secondary"
          aria-label="add ingredient"
          onClick={toggleModal}
          sx={{
            position: 'fixed',
            right: theme.spacing(6),
            bottom: theme.spacing(6),
            // default size * magnification rate
            width: 56 * addIngredientButtonMagnificationRate,
            height: 56 * addIngredientButtonMagnificationRate,
          }}
        >
          <AddIcon />
        </Fab>
      )}
      <Modal
        contentLabel="Register Ingredient"
        isOpen={modalIsOpen}
        onRequestClose={toggleModal}
        style={modalStyle}
      >
        <Container maxWidth="sm">
          <Typography variant="h4" textAlign="center" sx={{ pb: 3 }}>
            Add Ingredient
          </Typography>
          <IngredientForm onSubmit={onSubmit} manualOnly />
        </Container>
      </Modal>
    </React.Fragment>
  );
};

export default MyIngredientsPage;
