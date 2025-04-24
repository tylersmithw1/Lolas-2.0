import { Box, Typography, FormGroup, FormControlLabel, Checkbox, Button, Drawer } from "@mui/material";

const FilterDrawer = ({ open, onClose, selectedFilters, handleFilterChange, applyFilters }) => {
  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <Box sx={{ width: 250, padding: 2 }}>
        <Typography variant="h6" gutterBottom>
          Dietary Preferences
        </Typography>
        <FormGroup>
          {Object.entries(selectedFilters).map(([key, value]) => (
            <FormControlLabel
              key={key}
              control={<Checkbox checked={value} onChange={handleFilterChange} name={key} />}
              label={key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
            />
          ))}
        </FormGroup>
        <Box sx={{ mt: 2 }}>
          <Button variant="contained" fullWidth onClick={applyFilters}>
            Apply Filters
          </Button>
        </Box>
      </Box>
    </Drawer>
  );
};

export default FilterDrawer;
