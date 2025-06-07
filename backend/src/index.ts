import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import imageRoutes from './routes/imageRoutes';
import propertyRoutes from './routes/propertyRoutes';

// Load environment variables from .env file
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check route
app.get('/health', (_req, res) => {
  res.status(200).json({ status: 'ok', message: 'HouseFinder backend is running!' });
});

app.use('/api/image', imageRoutes);
app.use('/api/property', propertyRoutes);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
}); 