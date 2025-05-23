import { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import {
  Container,
  Grid,
  Typography,
  Box,
  Button,
  Divider,
  Paper,
  Tabs,
  Tab,
  Card,
  CardMedia,
  Breadcrumbs,
  Link,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  TextField,
  IconButton,
  Radio,
  FormControlLabel,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";
import ProductCard from "../components/ProductCard";

function ProductDetail() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [aiRecs, setAIRecs] = useState([]);
  const [relatedLoaded, setRelatedLoaded] = useState(false);
  const [aiLoaded, setAiLoaded] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState("sugar"); // defaults to low sugar rec
  const [openDialog, setOpenDialog] = useState(false);
  const [noRelatedProducts, setNoRelatedProducts] = useState(false);
  const [noAIProducts, setNoAIProducts] = useState(false);

  const options = [
    "sugar",
    "calories",
    "saturated fat",
    "sodium",
    "ultraprocessed",
    "nns",
  ];

  useEffect(() => {
    const fetchRelatedProducts = async () => {
      try {
        const response = await fetch("http://localhost:8000/recommendations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            product_name: product.name,
            column_name: selectedFilter,
          }),
        });

        if (!response.ok) throw new Error("Failed to fetch recommendations!");
        const data = await response.json();
        console.log(data);

        setRelatedProducts(data.products);
        setRelatedLoaded(true);
        setNoRelatedProducts(data.products.length === 0);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching related products:", error);
        setRelatedLoaded(true);
        setNoRelatedProducts(true);
      }
    };

    if (product && selectedFilter) {
      fetchRelatedProducts();
    }
  }, [product, selectedFilter]);

  useEffect(() => {
    const fetchAIRecs = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/ai-recommendations",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              full_product_name: product.name,
            }),
          },
        );

        if (!response.ok)
          throw new Error("Failed to fetch ai recommendations!");
        const data = await response.json();

        setAIRecs(data.products);
        setAiLoaded(true);
        setNoAIProducts(data.products.length === 0);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching ai recommendations:", error);
        setAiLoaded(true);
        setNoAIProducts(true);
      }
    };

    if (product) {
      fetchAIRecs();
    }
  }, [product]);

  useEffect(() => {
    setLoading(true);
    setRelatedLoaded(false);
    setAiLoaded(false);

    // If product data was passed via navigation state, use it
    if (location.state) {
      console.log(location.state);
      setProduct({
        ...location.state,
      });
    } else {
      // Fetch product details from API
      const fetchProductDetails = async () => {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/product-detail/${id}`,
            {
              method: "GET",
              headers: { "Content-Type": "application/json" },
            },
          );

          if (!response.ok) throw new Error("Failed to fetch product details");

          const data = await response.json();
          setProduct({
            ...data,
            description:
              data.description || "Product description not available",
            nutrition: data.nutrition || {
              calories: "Information not available",
              servingSize: "Information not available",
              protein: "Information not available",
              fat: "Information not available",
              carbs: "Information not available",
              fiber: "Information not available",
            },
          });
        } catch (error) {
          console.error("Error fetching product details:", error);
        } finally {
          setLoading(false);
        }
      };

      fetchProductDetails();
    }
  }, [id, location.state]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleQuantityChange = (event) => {
    const value = parseInt(event.target.value);
    if (!isNaN(value) && value > 0) {
      setQuantity(value);
    }
  };

  const incrementQuantity = () => {
    setQuantity((prevQuantity) => prevQuantity + 1);
  };

  const decrementQuantity = () => {
    if (quantity > 1) {
      setQuantity((prevQuantity) => prevQuantity - 1);
    }
  };

  const handleFilterChange = (event) => {
    setSelectedFilter(event.target.value);
  };

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const switchProductsWhenLoaded = (product) => {
    if (!relatedLoaded || !aiLoaded) {
      handleOpenDialog();
    } else {
      navigate(`/product/${encodeURIComponent(product.product)}`, {
        state: {
          name: product.product,
          price: product.price,
          image: `/images/${product.image}`,
          protein: product.protein,
          calories: product.energykcal,
          dietary_fiber: product.fibre,
          serving_size: product.servingsize,
          total_carbohydrates: product.carbohydrates,
          total_fat: product.fat,
          sugar: product.sugar,
          sodium: product.salt,
        },
      });
      setTimeout(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
      }, 0);
    }
  };

  // this was for when the page was loading but it doesn't really take long so i don't think we'd need this
  // if (loading) {
  //   return (
  //     <Container sx={{ py: 8, textAlign: 'center' }}>
  //       <CircularProgress size={60} />
  //       <Typography variant="h5" sx={{ marginTop: 2 }}>
  //         Loading product details...
  //       </Typography>
  //     </Container>
  //   );
  // }

  if (!product) {
    return (
      <Container sx={{ py: 8, textAlign: "center" }}>
        <Typography variant="h5">Product not found</Typography>
        <Button
          variant="contained"
          sx={{ mt: 2 }}
          onClick={() => navigate("/")}
        >
          Return to Home
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs
        separator={<NavigateNextIcon fontSize="small" />}
        aria-label="breadcrumb"
        sx={{ mb: 3 }}
      >
        <Link
          underline="hover"
          color="inherit"
          onClick={() => navigate("/")}
          sx={{ cursor: "pointer" }}
        >
          Home
        </Link>
        <Typography color="text.primary">{product.name}</Typography>
      </Breadcrumbs>

      {/* Product Details Section */}
      <Grid container spacing={4}>
        {/* Product Image */}
        <Grid item xs={12} md={6}>
          <Paper
            elevation={0}
            sx={{
              height: "100%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: "#f5f5f5",
              borderRadius: 2,
              p: 2,
            }}
          >
            <Box
              component="img"
              sx={{
                maxHeight: "400px",
                maxWidth: "100%",
                objectFit: "contain",
              }}
              src={product.image || "/images/product-placeholder.jpg"}
              alt={product.name}
            />
          </Paper>
        </Grid>

        {/* Product Information */}
        <Grid item xs={12} md={6}>
          <Typography
            variant="h4"
            component="h1"
            gutterBottom
            sx={{ fontFamily: "Garamond, serif" }}
          >
            {product.name}
          </Typography>

          <Typography
            variant="h5"
            color="primary"
            sx={{ mb: 2, fontWeight: "bold" }}
          >
            ${product.price ? product.price.toFixed(2) : "Price not available"}
          </Typography>

          <Typography variant="body1" paragraph>
            {product.description}
          </Typography>

          <Divider sx={{ my: 2 }} />

          {/* Quantity Selector */}
          <Box sx={{ display: "flex", alignItems: "center", mb: 3 }}>
            <Typography variant="body1" sx={{ mr: 2 }}>
              Quantity:
            </Typography>
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <IconButton size="small" onClick={decrementQuantity}>
                <RemoveIcon fontSize="small" />
              </IconButton>
              <TextField
                size="small"
                inputProps={{
                  min: 1,
                  style: { textAlign: "center" },
                }}
                value={quantity}
                onChange={handleQuantityChange}
                sx={{ width: "60px", mx: 1 }}
              />
              <IconButton size="small" onClick={incrementQuantity}>
                <AddIcon fontSize="small" />
              </IconButton>
            </Box>
          </Box>

          {/* Add to Cart Button */}
          <Button
            variant="contained"
            fullWidth
            size="large"
            sx={{
              backgroundColor: "#4a7c59",
              "&:hover": { backgroundColor: "#3a6349" },
              py: 1.5,
            }}
          >
            Add to Cart
          </Button>
        </Grid>
      </Grid>

      {/* Tabs Section */}
      <Box sx={{ mt: 6, mb: 4 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          centered
          sx={{ borderBottom: 1, borderColor: "divider" }}
        >
          <Tab label="Description" />
          <Tab label="Nutrition Facts" />
          <Tab label="Reviews" />
        </Tabs>

        {/* Tab Panels */}
        <Box sx={{ py: 3 }}>
          {tabValue === 0 && (
            <Typography variant="body1" paragraph>
              {product.description}
              <br />
              <br />
              Our products are sourced from trusted farmers and suppliers who
              share our commitment to quality and sustainability. We believe
              that what you put in your body matters, and we're dedicated to
              providing options that support your well-being and the health of
              our planet.
            </Typography>
          )}
          {tabValue === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Nutrition Information
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Serving Size</Typography>
                    <Typography variant="body1">
                      {product.serving_size}
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Calories</Typography>
                    <Typography variant="body1">
                      {product.calories} cal
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Protein</Typography>
                    <Typography variant="body1">{product.protein} g</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Total Fat</Typography>
                    <Typography variant="body1">
                      {product.total_fat} g
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">
                      Total Carbohydrates
                    </Typography>
                    <Typography variant="body1">
                      {product.total_carbohydrates} g
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Dietary Fiber</Typography>
                    <Typography variant="body1">
                      {product.dietary_fiber} g
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Sugar</Typography>
                    <Typography variant="body1">{product.sugar} g</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Sodium</Typography>
                    <Typography variant="body1">{product.sodium} g</Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          )}
          {tabValue === 2 && (
            <Box>
              <Typography variant="body1" paragraph>
                No reviews yet. Be the first to review this product!
              </Typography>
              <Button variant="outlined">Write a Review</Button>
            </Box>
          )}
        </Box>
      </Box>

      <Divider sx={{ my: 4 }} />

      {/* Filter Section */}
      <Box sx={{ my: 3 }}>
        <Typography variant="h6" gutterBottom>
          Select an option to tailor your recommendations:
        </Typography>
        <List>
          {options.map((option) => (
            <ListItem key={option}>
              <FormControlLabel
                control={
                  <Radio
                    checked={selectedFilter === option}
                    onChange={handleFilterChange}
                    value={option}
                  />
                }
                label={option}
              />
            </ListItem>
          ))}
        </List>
      </Box>

      <Divider sx={{ my: 4 }} />

      {/* Related Recommendations */}
      {relatedLoaded ? (
        <>
          <Typography variant="h5" gutterBottom>
            Tailored Recommendations by{" "}
            {selectedFilter === "nns"
              ? "NNS"
              : selectedFilter === "sugar"
                ? "Low Sugar"
                : selectedFilter === "calories"
                  ? "Low Calories"
                  : selectedFilter === "saturated fat"
                    ? "Low Saturated Fat"
                    : selectedFilter === "sodium"
                      ? "Low Sodium"
                      : selectedFilter === "ultraprocessed"
                        ? "Non-Ultraprocessed"
                        : ""}
          </Typography>
          <Divider sx={{ my: 4 }} />
          {noRelatedProducts ? (
            <Typography>
              No tailored recommendations available for this product.
            </Typography>
          ) : (
            <Grid container spacing={3}>
              {relatedProducts.map((product, index) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                  <ProductCard
                    name={product.product || "Unknown Product"}
                    price={product.price || 0}
                    protein={product.protein}
                    calories={product.energykcal}
                    dietary_fiber={product.fibre}
                    serving_size={product.servingsize}
                    total_carbohydrates={product.carbohydrates}
                    total_fat={product.fat}
                    sugar={product.sugar}
                    sodium={product.salt}
                    image={`/images/${product.image}`}
                    onClick={() => switchProductsWhenLoaded(product)}
                  />
                </Grid>
              ))}
            </Grid>
          )}
        </>
      ) : (
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            minHeight: 300,
          }}
        >
          <CircularProgress size={60} />
          <Typography sx={{ marginTop: 2 }}>
            Loading tailored recommendations...
          </Typography>
        </Box>
      )}

      <Divider sx={{ my: 4 }} />

      {/* AI Recommendations */}
      {aiLoaded ? (
        <>
          <Typography variant="h5" gutterBottom>
            AI Recommendations
          </Typography>
          <Divider sx={{ my: 4 }} />
          {noAIProducts ? (
            <Typography>
              No AI recommendations available for this product.
            </Typography>
          ) : (
            <Grid container spacing={3}>
              {aiRecs.map((product, index) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                  <ProductCard
                    name={product.product || "Unknown Product"}
                    price={product.price || 0}
                    protein={product.protein}
                    calories={product.energykcal}
                    dietary_fiber={product.fibre}
                    serving_size={product.servingsize}
                    total_carbohydrates={product.carbohydrates}
                    total_fat={product.fat}
                    sugar={product.sugar}
                    sodium={product.salt}
                    image={`/images/${product.image}`}
                    onClick={() => switchProductsWhenLoaded(product)}
                  />
                </Grid>
              ))}
            </Grid>
          )}
        </>
      ) : (
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            minHeight: 300,
          }}
        >
          <CircularProgress size={60} />
          <Typography sx={{ marginTop: 2 }}>
            Loading AI recommendations...
          </Typography>
        </Box>
      )}

      {/* Dialog for waiting until recommendations are fully loaded */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Wait for recommendations to load</DialogTitle>
        <DialogContent>
          <Typography>
            Please wait while we load the recommendations for this product. Once
            they are loaded you may proceed.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default ProductDetail;
